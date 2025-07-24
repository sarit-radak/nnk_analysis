import os
import pandas as pd

hist_dir = '2_paired/hist'
output_file = '2_paired/pair_summary.xlsx'

summary_data = []

for filename in os.listdir(hist_dir):
    if filename.endswith('.hist'):
        sample_name = filename.replace('_L001.hist', '')
        file_path = os.path.join(hist_dir, filename)
        
        stats = {
            'Sample': sample_name,
            'Mean': None,
            'Median': None,
            'Mode': None,
            'STDev': None,
            'PercentOfPairs': None
        }

        with open(file_path, 'r') as f:
            for line in f:
                if line.startswith('#Mean'):
                    stats['Mean'] = float(line.split()[1])
                elif line.startswith('#Median'):
                    stats['Median'] = int(line.split()[1])
                elif line.startswith('#Mode'):
                    stats['Mode'] = int(line.split()[1])
                elif line.startswith('#STDev'):
                    stats['STDev'] = float(line.split()[1])
                elif line.startswith('#PercentOfPairs'):
                    stats['PercentOfPairs'] = float(line.split()[1])
        
        summary_data.append(stats)

# Write to Excel
df = pd.DataFrame(summary_data)
df.to_excel(output_file, index=False)