import pandas as pd

# results = pd.read_csv('src/results_summary_final.csv')
# print(results)

from river import datasets

dsets_binary = {
    'Phishing': datasets.Phishing(),
    'Bananas': datasets.Bananas(),
    'CreditCard': datasets.CreditCard(),
    'Elec2': datasets.Elec2(),
    'HTTP': datasets.HTTP(),
    # 'MaliciousURL': datasets.MaliciousURL(),
    'SMTP': datasets.SMTP(),
    # 'SMSSpam': datasets.SMSSpam(),
    # 'TREC07': datasets.TREC07()
}

for dataset_name, dataset in dsets_binary.items():
    print(dataset_name)
    print(dataset.n_samples)
    dataset.take(10000)
    # for x, y in dataset.take(1):
    #     print(x)

