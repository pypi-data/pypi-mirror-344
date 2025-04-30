from sier2 import Info

def blocks() -> list[Info]:
    return [
        Info('sier2_blocks_datamap.blocks.umap:RunUMAP', 'Run data through UMAP to reduce dimensionality.'),
        Info('sier2_blocks_datamap.blocks.thisnotthat:ThisNotThat', 'Show a ThisNotThat interactive plot.'),
    ]

def dags() -> list[Info]:
    return [ 
        Info('sier2_blocks_datamap.dags.datamap:datamap', 'Load a dataframe and make a datamap'),
    ]
