#!/usr/bin/env python3
import os

from aws_cdk import core

from sprint5.sprint5_stack import Sprint5Stack
from sprint5.shanawar_pipeline_stack import PipelineStack

app = core.App()
PipelineStack(app,"shanawaralipipeline",env=core.Environment(account='315997497220',region='us-east-2'))

app.synth()
