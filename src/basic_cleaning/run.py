#!/usr/bin/env python
"""
Download from W&B the raw dataset and apply some basic data cleaning, exporting the result to a new artifact
"""
import argparse
import logging
import wandb
import pandas as pd

from wandb_utils.log_artifact import log_artifact

logging.basicConfig(level=logging.INFO, format="%(asctime)-15s %(message)s")
logger = logging.getLogger()


def go(args):

    run = wandb.init(job_type="basic_cleaning")
    run.config.update(args)

    # Download input artifact. This will also log that this script is using this
    # particular version of the artifact
    # artifact_local_path = run.use_artifact(args.input_artifact).file()

    ######################
    # YOUR CODE HERE     #
    ######################

    logger.info(f"Min price is  {args.min_price}")
    logger.info(f"Max price is  {args.max_price}")
    # logger.info(f"Uploading {args.artifact_name} to Weights & Biases")

    run = wandb.init(project="nyc_airbnb", group="basic_cleaning", save_code=True)
    local_path = wandb.use_artifact(args.input_artifact).file()
    df = pd.read_csv(local_path)

    # Drop outliers
    min_price = args.min_price
    max_price = args.max_price
    idx = df['price'].between(min_price, max_price)
    df = df[idx].copy()
    # Convert last_review to datetime
    df['last_review'] = pd.to_datetime(df['last_review'])

    df.to_csv(args.output_artifact, index=False)

    log_artifact(
        args.output_artifact,
        args.output_type,
        args.output_description,
        args.output_artifact,
        run,
    )


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="A very basic data cleaning")


    parser.add_argument(
        "--input_artifact", 
        type=str,
        help='Raw data csv file',
        required=True
    )

    parser.add_argument(
        "--output_artifact", 
        type=str,
        help='Name of the output csv file',
        required=True
    )

    parser.add_argument(
        "--output_type", 
        type=str,
        help='Type of the output file',
        required=True
    )

    parser.add_argument(
        "--output_description", 
        type=str,
        help="Description of the file",
        required=True
    )

    parser.add_argument(
        "--min_price", 
        type=int,
        help="Minimum price of the rooms",
        required=True
    )

    parser.add_argument(
        "--max_price", 
        type=int,
        help='Maximum price of the rooms',
        required=True
    )


    args = parser.parse_args()

    go(args)
