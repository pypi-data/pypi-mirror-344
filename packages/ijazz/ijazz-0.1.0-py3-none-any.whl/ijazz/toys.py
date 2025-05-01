__doc__ = "This module allows to create a simple MC simulation of the Z->ee decay" \
          "with a gaussian smearing and scale shift that can be tune w/r " \
          "to a property x which is generated in the range [0., 100.]" \
          "Author: fabrice.couderc@cea.fr" \
          "Revision: v1 - 21/03/2024"


from ijazz.dtypes import floatzz
import tensorflow as tf
import tensorflow_probability as tfp
import numpy as np, pandas as pd


mass_z = tf.constant(91.1876, dtype=floatzz)
gamma_z = tf.constant(2.4952, dtype=floatzz)
win_z_mc = (50, 130)
win_z_dt = (70, 110)


def decalibrate(x):
    """
    Decalibrate the response of the events for the property x
    :param x: (np.array) property
    :return:
    """
    return 1 + x/1000 * tf.sin(x/5)


def oversmearing(x):
    """
    Additional oversmearing according to property x
    :param x: (np.array) property
    :return:
    """
    return np.ones(x.shape) * 0.020


# -- oversmearing function more realistic
def oversmearing2(x):
    # return 0.015 * np.ones(tf.shape(x))
    return 0.015 * (1 + (x / 100) ** 2)


def dataset(do_decal, n_toys=100, decalibrate_f=decalibrate, oversmearing_f=oversmearing,
            smear_property=False, prop_gaus=False, return_smear=False):
    """
    create the dataset
    :param prop_gaus: gaussian shape for the property (mean 45 and sigma = 25)
    :param do_decal: decalibrate the Z BW evts using the decalibrte_f and oversmearing_f functions
    :param n_toys: number of MC toys
    :param decalibrate_f: scale decalibration function
    :param oversmearing_f: oversmearing function
    :param smear_property: smear the properties x1 and x2 according to the smearing in the mass

    :return: tf.tensor(n_toys, ), x1, x2 with x1 and x2 the x properties of the 2 electrons
    """

    mee_bw = tf.cast(tfp.distributions.Cauchy(mass_z, gamma_z / 2.).sample(n_toys), floatzz)
    # e1_smear = tf.ones(n_toys, dtype=floatzz)
    # e2_smear = tf.ones(n_toys, dtype=floatzz)
    e1_smear = np.random.normal(1, 0.02, n_toys)
    e2_smear = np.random.normal(1, 0.02, n_toys)
    mee_smear = mee_bw * tf.sqrt(e1_smear * e2_smear)
    prop_min = 0
    prop_max = 100

    # -- generate properties with a larger range than [prop_min, prop_max], so it can be randomized
    if prop_gaus:
        x1 = tf.cast(tfp.distributions.Normal(45, 18).sample(n_toys), floatzz)
        x2 = tf.cast(tfp.distributions.Normal(45, 18).sample(n_toys), floatzz)
    else:
        x1 = tf.cast(tfp.distributions.Uniform(prop_min-10, prop_max+10).sample(n_toys), floatzz)
        x2 = tf.cast(tfp.distributions.Uniform(prop_min-10, prop_max+10).sample(n_toys), floatzz)

    if do_decal:
        corr1 = decalibrate_f(x1)
        corr2 = decalibrate_f(x2)
        e1_os = np.random.normal(1, oversmearing_f(x1))
        e2_os = np.random.normal(1, oversmearing_f(x2))
        mee_smear *= tf.sqrt(corr1 * corr2 * e1_os * e2_os)
        if smear_property:
            x1 *= corr1 * e1_os
            x2 *= corr2 * e2_os
        s1 = corr1 * e1_os
        s2 = corr2 * e2_os

    win_z = win_z_mc
    if do_decal:
        win_z = win_z_dt
        sel_dt = (mee_smear >= win_z[0]) & (mee_smear <= win_z[1])
        mee_smear = mee_smear[sel_dt]
        x1 = x1[sel_dt]
        x2 = x2[sel_dt]
        s1 = s1[sel_dt]
        s2 = s2[sel_dt]

    # -- force x1 and x2 to be in [0, 100] after potential x1 and x2 smearing
    sel = (x1 >= prop_min) & (x2 >= prop_min) & (x1 < prop_max) & (x2 < prop_max)
    x1 = x1[sel]
    x2 = x2[sel]
    if do_decal:
        s1 = s1[sel]
        s2 = s2[sel]
    mee_smear = mee_smear[sel]
    if return_smear :
        return tf.clip_by_value(mee_smear, *win_z), x1, x2, s1, s2
    
    else :
        return tf.clip_by_value(mee_smear, *win_z), x1, x2


# --------------------------------------------------------------------------
# - Next section adresses the Pythia simulation (decalibration and smearing)
# --------------------------------------------------------------------------

def tree_to_df(tree, random_R9=True, use_fabrice=False):
    mc_m_z, mc_pt_z, mc_pt_e1_true, mc_pt_e2_true, mc_y_e1_true, mc_y_e2_true, mc_phi_e1_true, mc_phi_e2_true = \
        tree_to_df_fabrice(tree) if use_fabrice else tree_to_df_paul(tree)

    if random_R9:
        r91 = np.random.normal(0.94, 0.1, len(mc_pt_e1_true))
        r92 = np.random.normal(0.94, 0.1, len(mc_pt_e1_true))
    
    sel = (mc_m_z > 50) & (mc_pt_z > 0) & (mc_pt_e1_true > 10) & (mc_pt_e2_true > 10) # -- minimum pT cut added 
    df = pd.DataFrame({'mee_true': mc_m_z[sel], 'pT_Z': mc_pt_z[sel], 
                        'pT1_true': mc_pt_e1_true[sel], 'pT2_true': mc_pt_e2_true[sel],
                        'y1': mc_y_e1_true[sel], 'abs_y1': abs(mc_y_e1_true[sel]),
                        'y2': mc_y_e2_true[sel], 'abs_y2': abs(mc_y_e2_true[sel]),
                        'phi1': mc_phi_e1_true[sel], 'phi2': mc_phi_e2_true[sel],
                        'R91': r91[sel], 'R92': r92[sel],})

    return df

def tree_to_df_paul(tree):
    mc_pt_e_i_true = tree["pT_e_i"].array(library="np")
    mc_y_e_i_true = tree["y_e_i"].array(library="np")
    mc_phi_e_i_true = tree["phi_e_i"].array(library="np")
    mc_id_e_i_true = tree["id_e_i"].array(library="np")
    mc_m_Z = tree["m_Z"].array(library="np")
    mc_m_Z_true = mc_m_Z[mc_m_Z>0]
    mc_pT_Z = tree["pT_Z"].array(library="np")
    mc_pT_Z = mc_pT_Z[mc_m_Z>0]

    #electrons
    mc_pt_e1_true = mc_pt_e_i_true[mc_id_e_i_true==11]
    mc_y_e1_true = mc_y_e_i_true[mc_id_e_i_true==11]
    mc_phi_e1_true = mc_phi_e_i_true[mc_id_e_i_true==11]

    #positrons
    mc_pt_e2_true = mc_pt_e_i_true[mc_id_e_i_true==-11]
    mc_y_e2_true = mc_y_e_i_true[mc_id_e_i_true==-11]
    mc_phi_e2_true = mc_phi_e_i_true[mc_id_e_i_true==-11]

    return mc_m_Z, mc_m_Z_true, mc_pt_e1_true, mc_pt_e2_true, mc_y_e1_true, mc_y_e2_true, mc_phi_e1_true, mc_phi_e2_true

def tree_to_df_fabrice(tree):
    mc_pt_e_i_true = tree["pt_top"].array(library="np")
    mc_y_e_i_true = tree["eta_top"].array(library="np")
    mc_phi_e_i_true = tree["phi_top"].array(library="np")

    #electrons
    i_ele = 0
    mc_pt_e1_true = mc_pt_e_i_true[:, i_ele]
    mc_y_e1_true = mc_y_e_i_true[:, i_ele]
    mc_phi_e1_true = mc_phi_e_i_true[:, i_ele]

    #positrons
    i_ele = 1
    mc_pt_e2_true = mc_pt_e_i_true[:, i_ele]
    mc_y_e2_true = mc_y_e_i_true[:, i_ele]
    mc_phi_e2_true = mc_phi_e_i_true[:, i_ele]

    mc_m_z = np.sqrt(2*mc_pt_e1_true*mc_pt_e2_true*
            (np.cosh(mc_y_e1_true-mc_y_e2_true) - 
            np.cos(mc_phi_e1_true-mc_phi_e2_true)))

    mc_pt_z = np.sqrt(mc_pt_e1_true**2 + mc_pt_e2_true**2 + 
            2*mc_pt_e1_true*mc_pt_e2_true* 
            np.cos(mc_phi_e1_true-mc_phi_e2_true))

    return mc_m_z, mc_pt_z, mc_pt_e1_true, mc_pt_e2_true, mc_y_e1_true, mc_y_e2_true, mc_phi_e1_true, mc_phi_e2_true

def detector_smearing(x1, x2, mee, sigma=0.02):
    """add smearing of resolution sigma to x1, x1 and mee

    :param x1: variable to apply the smearing (first electron)
    :param x2: variable to apply the smearing (second electron)
    :param mee: variable to apply the smearing (dilepton system)
    :param sigma: gaussian resolution, defaults to 0.02
    :return: x1_smear, x2_smear, mee_smear the smeared variables
    """
    e1_os = np.random.normal(1, sigma, len(x1))
    e2_os = np.random.normal(1, sigma, len(x1))
    mee_smear = mee * np.sqrt(e1_os * e2_os)
        
    x1_smear = x1 * e1_os
    x2_smear = x2 * e2_os
    

    return x1_smear, x2_smear, mee_smear

def decal_and_os(x1, x2, pT1, pT2, mee, decalibrate_f=decalibrate, oversmearing_f=oversmearing, decal_kwargs={}, os_kwargs={}):
    """decalibrate and add oversmearing to pT1, pT2 and mee

    :param x1: tuple of variables to use as input for the decalibrate and oversmearing functions (first lepton)
    :param x2: tuple of variables to use as input for the decalibrate and oversmearing functions (second lepton)
    :param pT1: variable to apply the decalibration and oversmearing (first lepton)
    :param pT2: variable to apply the decalibration and oversmearing (second lepton)
    :param mee: variable to apply the decalibration and oversmearing (dilepton system)
    :param decalibrate_f: function to decalibrate the pT, defaults to decalibrate
    :param oversmearing_f: function to oversmear the pT, defaults to oversmearing_all
    :return: pT1_smear, pT2_smear, mee_smear, mee_os (mee with only os) the smeared variables
    """
    corr1 = decalibrate_f(*x1, **decal_kwargs)
    corr2 = decalibrate_f(*x2, **decal_kwargs)
    e1_os = np.random.normal(1, oversmearing_f(*x1, **os_kwargs))
    e2_os = np.random.normal(1, oversmearing_f(*x2, **os_kwargs))
    mee_os = mee * np.sqrt(e1_os * e2_os)
    mee_smear = mee * np.sqrt(corr1 * corr2 * e1_os * e2_os)
    
    pT1_smear = pT1* corr1 * e1_os
    pT2_smear = pT2* corr2 * e2_os

    return pT1_smear, pT2_smear, mee_smear, mee_os