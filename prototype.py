import pandas as pd

frame = 'data/2021-02-23_Villa_8-4.csv'

indices = ["MATCH OVERVIEW", "MATCH PERFORMANCE", "SIXTH PICK OVERVIEW", "PLAYER ROUNDS DATA", "ROUND EVENTS BREAKDOWN"]
indices_no = [0]
frame_depth = []
unfiltered_frame = pd.read_csv(frame, sep=';')
row_count = unfiltered_frame.shape[0]

for idx, name in enumerate(indices):
    sniffer_no = 0
    for row_no in range(0, row_count):
        row_content = unfiltered_frame.iloc[row_no, 0]
        if name in row_content:
            indices_no.append(sniffer_no)
            frame_depth.append((sniffer_no-indices_no[idx]))

        sniffer_no += 1
frame_depth.append(row_count-indices_no[len(indices_no)-1])
indices = ["BEGINN"] + indices
for idx, x in enumerate(indices_no):
    indices_no[idx] = x + 2
for idx, x in enumerate(frame_depth):
    frame_depth[idx] = x - 2
indexFrame = pd.DataFrame(list(zip(indices, indices_no, frame_depth)),
                          columns =['Name', 'Index', 'Depth'])

print(indexFrame)
print(indexFrame["Index"][1])


df = pd.read_csv(frame, sep='\,', header=None, skiprows=4, nrows=2, engine='python')
print(df)