import logging
from bid_shading_e_e import BidShading
import argparse


def main(mdate, method_name):
    bs = BidShading(logging, mdate, method_name)
    bs.run()


if __name__ == '__main__':
    # python3 bid_shading_e_e.py > train.log 2>&1 &
    parser = argparse.ArgumentParser(description="bid shading experiment")
    # add args
    parser.add_argument("-mdate", default="20221019")
    parser.add_argument("-method_name", default="UCB_exp_abs")
    args = parser.parse_args()
    print(args)

    for mdate in ["20221015", "20221016", "20221017", "20221018", "20221019", "20221020", "20221021"]:
        main(mdate, args.method_name)