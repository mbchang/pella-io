import requests
import json
import time

def main():
    all_probs = dict()
    # for cp in ['1']:
    for cp in ['1', '2', '3', '4', '5', '6', '7']:
        r = requests.get("https://api.hooktheory.com/v1/trends/nodes?cp="+str(cp), headers={"Authorization": "Bearer 18c7027351e70830752fd8da22ca0e9b"})
        j = json.loads(r.content)
        probs_cp = dict()
        for i in j:
            if len(i["chord_ID"]) == 1:
                probs_cp[str(i["chord_ID"])] = i["probability"] 

        allsum = sum(probs_cp.values()) 
        probs_cp[cp] = 1 - allsum

        print probs_cp 
        all_probs[cp] = probs_cp
        time.sleep(2)

    return all_probs

if __name__ == '__main__':
    # all_probs = main()
    # print all_probs 
    # print json.dumps(all_probs)
    print dict(json.loads('{"1": {"1": 0.364, "3": 0.036, "2": 0.061, "5": 0.254, "4": 0.183, "7": 0.003, "6": 0.099}, "3": {"1": 0.05, "3": 0.20299999999999996, "2": 0.082, "5": 0.074, "4": 0.319, "7": 0, "6": 0.272}, "2": {"1": 0.126, "3": 0.087, "2": 0.29200000000000004, "5": 0.156, "4": 0.156, "7": 0.001, "6": 0.182}, "5": {"1": 0.211, "3": 0.039, "2": 0.064, "5": 0.21799999999999997, "4": 0.205, "7": 0.001, "6": 0.262}, "4": {"1": 0.29, "3": 0.044, "2": 0.048, "5": 0.289, "4": 0.2340000000000001, "7": 0.002, "6": 0.093}, "7": {"1": 0.237, "3": 0.036, "2": 0.006, "5": 0.053, "4": 0.041, "7": 0.40900000000000003, "6": 0.218}, "6": {"1": 0.107, "3": 0.06, "2": 0.061, "5": 0.203, "4": 0.233, "7": 0.005, "6": 0.33099999999999996}}'))

