import pandas as pd
import os
import glob

# replace with your folder's path
folder_path = r'./datasets/ava_frame/'

all_files = os.listdir(folder_path)

# Filter out non-CSV files
csv_files = ['output_values1.csv', 'output_values2.csv', 'output_values3.csv', 'output_values4.csv', 'output_values5.csv', 'output_values6.csv', 
            'output_values7.csv', 'output_values8.csv', 'output_values9.csv', 'output_values10.csv', 'output_values11.csv', 'output_values12.csv']

print(csv_files)

# Create a list to hold the dataframes
df_list = []

for csv in csv_files:
    file_path = os.path.join(folder_path, csv)
    try:
        # Try reading the file using default UTF-8 encoding
        df = pd.read_csv(file_path)
        df_list.append(df)
    except UnicodeDecodeError:
        try:
            # If UTF-8 fails, try reading the file using UTF-16 encoding with tab separator
            df = pd.read_csv(file_path, sep='\t', encoding='utf-16')
            df_list.append(df)
        except Exception as e:
            print(f"Could not read file {csv} because of error: {e}")
    except Exception as e:
        print(f"Could not read file {csv} because of error: {e}")

# Concatenate all data into one DataFrame
big_df = pd.concat(df_list, ignore_index=True)

# Save the final result to a new CSV file
big_df.to_csv(os.path.join(folder_path, 'ava_frame_dataset.csv'), index=False)


for row in big_df:
    print(row)
    pictures = glob.glob(f'./datasets/ava_frame/frames/url_{row['url_id']}_sec{row['Second']}.jpg')
    if pictures:
        print('Trovato')
    else:
        big_df.drop(row) 


npfiles = ['annotations_values1.npy', 'annotations_values2.npy', 'annotations_values3.npy', 'annotations_values4.npy', 'annotations_values5.npy', 'annotations_values6.npy', 
            'annotations_values7.npy', 'annotations_values8.npy', 'annotations_values9.npy', 'annotations_values10.npy', 'annotations_values11.npy', 'annotations_values12.npy']
print(npfiles)
all_arrays = []
for npfile in npfiles:
    print(npfile)
    a = np.load(os.path.join('./datasets/ava_frame/annotations/', npfile))
    all_arrays.append(a)
    print(all_arrays)
all_array = np.array(all_arrays)
print(all_array)
np.save('ava_frame_dataset_target.npy', all_array)
