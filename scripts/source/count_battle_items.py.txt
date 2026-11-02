"""Count actual player bag-item uses from a completed native battle log.
Choices, enemy/partner use, and held activations are intentionally excluded.
Use only completed battle logs; this helper never inspects live battle decisions.
"""
from pathlib import Path
from collections import Counter
import re,json,argparse

def count_items(path):
    counts=Counter(re.findall(r'^\[Player used (.+)\]\s*$',Path(path).read_text(),re.M))
    return [{'name':name,'count':count} for name,count in sorted(counts.items())]

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('completed_log');a=p.parse_args()
    print(json.dumps({'item_usage':count_items(a.completed_log),'item_usage_evidence':{'method':'Exact completed native log [Player used ...] lines','source':a.completed_log,'scope':'Player bag consumables in this battle only'}},indent=2))
