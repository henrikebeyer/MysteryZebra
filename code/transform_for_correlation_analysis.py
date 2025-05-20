import pandas as pd

# dataframe with columns: norm_score, model-size, n, d, nxd, level

# read in all evaluation files

def prepare_data():

    model_dict = {"LLaMa3.1-70B":70, 
                "LLaMa3.3-70B":70, 
                "LLaMa3":8, 
                "Mistral":7, 
                "Qwen2":7, 
                "Qwen2-72B":72}

    family_dict = {"LLaMa3.1-70B":"Llama", 
                "LLaMa3.3-70B":"Llama", 
                "LLaMa3":"Llama", 
                "Mistral":"Mistral", 
                "Qwen2":"Qwen", 
                "Qwen2-72B":"Qwen"}

    df_list = []

    for model in list(model_dict.keys()):
        path = f"/home/oenni/Dokumente/LLM_reasoning/Model_testing/{model}-zeroShot/orig_puzzles/general_metrics/all_levels_orig_norm_scores.tsv"
        df = pd.read_csv(path, sep="\t")

        grid_acc = []
        n = []
        d = []
        dxn = []
        model_size = []
        level = []

        #sizes = 

        df["n"] = df["sizes"].str.split("x").str[1].astype(int)
        df["d"] = df["sizes"].str.split("x").str[0].astype(int)
        df["dxn"] = df["d"] * df["n"]
        df["parameters"] = [model_dict[model] for dummy in df["sizes"]]
        df["model"] = [model for dummy in df["sizes"]]

        perf_columns = [f"Lv{level}-norm_score" for level in range(1, 13)]
        for column, lv in zip(perf_columns, range(1,13)):
            grid_acc += list(df[column])
            n += list(df["n"])
            d += list(df["d"])
            dxn += list(df["dxn"])
            model_size += list(df["parameters"])
            level += [lv for dummy in df["n"]]

        out_df = pd.DataFrame()
        out_df["n"] = n
        out_df["d"] = d
        out_df["dxn"] = dxn
        out_df["grid_acc"] = grid_acc
        out_df["model_size"] = model_size
        out_df["level"] = level

        corr_df = out_df.corr()
        corr_df.to_csv(f"/home/oenni/Dokumente/LLM_reasoning/correlation_analysis/correlation_matrix_{model}.tsv", sep="\t", index=True)

        df_list.append(out_df)

    corr_df = pd.concat(df_list)

    out_path = "/home/oenni/Dokumente/LLM_reasoning/correlation_analysis/correlation_analysis_data.tsv"

    corr_df.to_csv(out_path, sep="\t", index=False)

prepare_data()

correlation_path = "/home/oenni/Dokumente/LLM_reasoning/correlation_analysis/correlation_analysis_data.tsv"
full_df = pd.read_csv(correlation_path, sep="\t")

corr_df = full_df.corr()

corr_df.to_csv("/home/oenni/Dokumente/LLM_reasoning/correlation_analysis/correlation_matrix_all.tsv", sep="\t", index=True)

