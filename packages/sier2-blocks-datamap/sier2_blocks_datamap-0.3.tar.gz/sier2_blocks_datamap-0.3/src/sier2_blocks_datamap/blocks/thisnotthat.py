from sier2 import Block
import param

import panel as pn
import numpy as np
import pandas as pd

from thisnotthat import BokehPlotPane

class ThisNotThat(Block):
    """ This Not That datamap viewer

    Use ThisNotThat to make an interactive viewer of a datamap.
    """
    
    in_df = param.DataFrame(doc='Input dataframe containing labels and hover text')
    in_map_data = param.Array(doc='Input map data')
    in_label_col = param.Selector(doc='Input label column')
    in_hover_col = param.Selector(doc='Input hover text column')

    def __init__(self, *args, block_pause_execution=True, **kwargs):
        super().__init__(*args, block_pause_execution=block_pause_execution, continue_label='Make TnT Plot', **kwargs)
        
        self.plot = pn.pane.Placeholder(sizing_mode='stretch_width')

    def prepare(self):
        self.param['in_label_col'].objects = self.in_df.columns
        self.param['in_hover_col'].objects = self.in_df.columns
        
    def execute(self):
        if None not in (self.in_label_col, self.in_hover_col):
            self.plot.update(BokehPlotPane(
                self.in_map_data,
                labels=self.in_df[self.in_label_col].astype(str),
                hover_text=self.in_df[self.in_hover_col].astype(str),
                sizing_mode='stretch_width',
            ))

    def __panel__(self):
        return pn.Row(
            pn.Param(
                self,
                parameters=['in_label_col', 'in_hover_col'],
            ),
            self.plot,
            sizing_mode='stretch_width',
        )


