def e_coh(e_bulk, e_atom, n_atom_bulk):
    """Calculate the cohesive energy of a bulk material.

    Keyword arguments:
    e_bulk -- total energy of the bulk structure.
    e_atom -- total energy of a isolated atom.
    n_atom_bulk -- number of atoms in the bulk.

    """
    return ((e_bulk) - (n_atom_bulk*e_atom)) / n_atom_bulk


def e_surf_form(e_t_surf, e_t_bulk, n_atoms_surf, n_atoms_bulk, area):
    """Calculate the surface formation energy per area of the surface.

    Keyword arguments:
    e_t_surf -- total energy of the surface slab.
    e_t_tbulk -- total energy of the bulk.
    n_atoms_surf -- number fo atoms in the slab unit cell.
    n_atoms bulk -- number of atoms in a bulk unit cell.
    area -- area of the slab.

    """
    return ((e_t_surf) - (n_atoms_surf*e_t_bulk / n_atoms_bulk))/(2*area)

def e_ads(n_ads, et_surf_ads, et_surf, et_ads):
        """"Calculate the adsorption energy per atom.

        Keyword arguments:
        n_ads -- number of adsorbates in the supercell.
        et_surf_ads -- total energy of the system containing the surface and
        the adsorbate.
        et_surf -- total energy of the system containing the clean slab.
        et_ads -- total energy of one atom/molecule of the adsorbate.

        """
        return ((et_surf_ads) - (n_ads * et_ads + et_surf)) / (n_ads)

def wf(vac_pot, e_fermi):
    """Calculate the work function"""
    return vac_pot - e_fermi

def d_center(slab_xml, vac_pot_slab, fermi_slab):
    """Calculate the d-band center of a structure

    Keyword arguments:
    slab_xml -- parsed vasprun.xml to be analysed.
    vac_pot_slab -- vacuum potential of the slab, or the Fermi energy of the
    slab.
    fermi_slab -- fermi energy extracted from vasprun.xml.

    """
    import numpy as np
    from pymatgen.io.vasp.outputs import Vasprun
    from pymatgen.electronic_structure.plotter import DosPlotter

    # Extracting the data using pymatgen DosPlotter
    plotter = DosPlotter(zero_at_efermi=False, stack=False, sigma=0.0)
    plotter.add_dos_dict(slab_xml.complete_dos.get_element_spd_dos('Ni'))
    dos_dict = plotter.get_dos_dict()

    # Converting the data into numpy arrays
    e_levels = np.asarray(list(dos_dict['d']['energies']))
    density_up = np.asarray(list(dos_dict['d']['densities']['1']))
    density_down = np.asarray(list(dos_dict['d']['densities']['-1']))
    norm_levels = e_levels - vac_pot_slab

    #Calculating the d-band center
    my_energies = norm_levels[np.where(
        norm_levels[:] < (fermi_slab - vac_pot_slab))]
    density_up_1 = density_up[:len(my_energies)]
    density_down_1 = density_down[:len(my_energies)]
    d_center_up = np.average(my_energies, weights=density_up_1)
    d_center_down = np.average(my_energies, weights=density_down_1)
    d_center_avg = (d_center_up + d_center_down) / 2
    return d_center_avg


def read_vasprun(data):
    """Read the file vasprun.xml for further analysis using pymatgen"""
    from pymatgen.io.vasp.outputs import Vasprun

    xml_vasp = Vasprun(data)
    print (xml_vasp)
    return xml_vasp
