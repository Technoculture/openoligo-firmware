from openoligo.container.cartridge import dna_cartridge, reagents, rna_cartridge


def test_dna_cartridge():
    dna_cartridge.atgc
    dna_cartridge.methylated


def test_rna_cartridge():
    rna_cartridge.augc
    rna_cartridge.methylated


def test_reagent():
    _ = reagents
    reagents.acetonitrile
