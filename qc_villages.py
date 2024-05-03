import pandas as pd

filename = "2024-05-02_Village_Regions.xlsx"
gov_filename = "GOV_Village_Regions.xlsx"
df_fs = pd.read_excel(filename, sheet_name="REGION_Village")
df_gov = pd.read_excel(gov_filename, sheet_name="data.gov.in")


df_fs["full_district_name"] = df_fs["r_001_state_name"].str.cat(
    df_fs[["r_002_dis_name"]], sep=":"
)
df_fs["full_taluka_name"] = df_fs["r_001_state_name"].str.cat(
    df_fs[
        [
            "r_002_dis_name",
            "r_003_tal_name",
        ]
    ],
    sep=":",
)
df_fs["full_village_name"] = df_fs["r_001_state_name"].str.cat(
    df_fs[
        [
            "r_002_dis_name",
            "r_003_tal_name",
            "r_004_vill_name",
        ]
    ],
    sep=":",
)

df_fs["full_district_name"] = df_fs["full_district_name"].str.lower()
df_fs["full_taluka_name"] = df_fs["full_taluka_name"].str.lower()
df_fs["full_village_name"] = df_fs["full_village_name"].str.lower()

fs_districts = df_fs["full_district_name"].unique().tolist()
fs_talukas = df_fs["full_taluka_name"].unique().tolist()
fs_villages = df_fs["full_village_name"].unique().tolist()


df_gov["full_district_name"] = df_gov["STATE NAME"].str.cat(
    df_gov[["DISTRICT NAME"]], sep=":"
)
df_gov["full_taluka_name"] = df_gov["STATE NAME"].str.cat(
    df_gov[["DISTRICT NAME", "SUB-DISTRICT NAME"]], sep=":"
)
df_gov["full_village_name"] = df_gov["STATE NAME"].str.cat(
    df_gov[["DISTRICT NAME", "SUB-DISTRICT NAME", "Area Name"]], sep=":"
)

df_gov["full_district_name"] = df_gov["full_district_name"].str.lower()
df_gov["full_taluka_name"] = df_gov["full_taluka_name"].str.lower()
df_gov["full_village_name"] = df_gov["full_village_name"].str.lower()
df_fs['r_001_state_name'] = df_fs['r_001_state_name'].str.lower()

dg_districts = df_gov["full_district_name"].unique().tolist()
dg_talukas = df_gov["full_taluka_name"].unique().tolist()
dg_villages = df_gov["full_village_name"].unique().tolist()

district_names = list(set(dg_districts).difference(set(fs_districts)))
taluka_names = list(set(dg_talukas).difference(set(fs_talukas)))
village_names = list(set(dg_villages).difference(set(fs_villages)))

district_names = sorted(district_names)
taluka_names = sorted(taluka_names)
village_names = sorted(village_names)

# dictionary of lists
fs_district_dict = {"fs_district": fs_districts}
fs_taluka_dict = {"fs_talukas": fs_talukas}
dg_district_dict = {"dg_district": dg_districts}
dg_taluka_dict = {"dg_talukas": dg_talukas}

fs_district_df = pd.DataFrame(fs_district_dict)
fs_taluka_df = pd.DataFrame(fs_taluka_dict)
dg_district_df = pd.DataFrame(dg_district_dict)
dg_taluka_df = pd.DataFrame(dg_taluka_dict)

diff_district_df = pd.DataFrame(district_names, columns=['Total'])
split_values = diff_district_df['Total'].str.split(pat=":", expand=True)
diff_district_df['State'] = split_values[0]
diff_district_df['District'] = split_values[1]
merged_df = pd.merge(df_fs, diff_district_df, left_on="r_001_state_name",right_on="State", how="right")
merged_df = merged_df.drop_duplicates(subset=['District'],keep='first')
merged_df = merged_df.drop(['best_match', 'Name_y'], axis=1)
# fs_district_df= fs_district_df.assign(State=lambda x: fs_district_df['Total'].str.split(pat=":")[0])



#

# diff_district_df = pd.DataFrame(diff_district_dict)
# diff_taluka_df = pd.DataFrame(diff_taluka_dict)
# diff_village_df = pd.DataFrame(diff_village_dict)
#
# fs_district_df = pd.DataFrame({"fs_state": fs_district_df.str.split(pat=":")[0], "fs_district": fs_district_df.str.split(pat=":")[1]})
# fs_taluka_df = pd.DataFrame({"fs_state": fs_taluka_df.str.split(pat=":")[0], "fs_district": fs_taluka_df.str.split(pat=":")[1],"fs_talukas": fs_taluka_df.str.split(pat=":")[2]})
# dg_district_df = pd.DataFrame({"dg_state": dg_district_df.str.split(pat=":")[0], "dg_district": dg_district_df.str.split(pat=":")[1]})
# dg_taluka_df = pd.DataFrame({"dg_state": dg_taluka_df.str.split(pat=":")[0], "dg_district": dg_taluka_df.str.split(pat=":")[1],"dg_talukas": dg_taluka_df.str.split(pat=":")[2]})
# diff_district_df = pd.DataFrame({"diff_state": diff_district_df.str.split(pat=":")[0], "diff_district": diff_district_df.str.split(pat=":")[1]})
# diff_taluka_df = pd.DataFrame({"diff_state": diff_taluka_df.str.split(pat=":")[0], "diff_district": diff_taluka_df.str.split(pat=":")[1],"diff_talukas": diff_taluka_df.str.split(pat=":")[2]})
# diff_village_df = pd.DataFrame({"diff_state": diff_village_df.str.split(pat=":")[0], "diff_district": diff_village_df.str.split(pat=":")[1],"diff_talukas": diff_village_df.str.split(pat=":")[2],"diff_villages": diff_village_df.str.split(pat=":")[3]})

with pd.ExcelWriter(f"QC_{filename}", engine="xlsxwriter") as writer:
    df_fs.to_excel(writer, sheet_name="FS", index=False)
    df_gov.to_excel(writer, sheet_name="GOV", index=False)
    fs_district_df.to_excel(writer, sheet_name="FS-DIS", index=False)
    fs_taluka_df.to_excel(writer, sheet_name="FS-TAL", index=False)
    dg_district_df.to_excel(writer, sheet_name="GOV-DIS", index=False)
    dg_taluka_df.to_excel(writer, sheet_name="GOV-TAL", index=False)
    diff_district_df.to_excel(writer, sheet_name="Diff-GOV-DIS", index=False)
    merged_df.to_excel(writer, sheet_name="Merged_-DIS", index=False)
    # diff_taluka_df.to_excel(writer, sheet_name="Diff-GOV-TAL", index=False)
    # diff_village_df.to_excel(writer, sheet_name="Diff-GOV-VIL", index=False)

print("Completed")
