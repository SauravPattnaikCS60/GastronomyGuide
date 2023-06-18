import ast

def clean_data(df):
    df = df[df['votes'] >= 1000].reset_index(drop=True)
    df = df[df['name'] != 'CafÃ\x83Â\x83Ã\x82Â\x83Ã\x83Â\x82Ã\x82Â\x83Ã\x83Â\x83Ã\x82Â\x82Ã\x83Â\x82Ã\x82Â© Felix'].reset_index(drop=True)
    print(f'Total no of records are {df.shape[0]}')
    df['rest_type'].fillna('', inplace=True)
    df['dish_liked'].fillna('', inplace=True)
    df['cuisines'].fillna('', inplace=True)
    df['approx_cost(for two people)'].fillna(-1, inplace=True)

    df['rest_type'] = df['rest_type'].apply(lambda x: x.split(','))
    df['dish_liked'] = df['dish_liked'].apply(lambda x: x.split(','))
    df['cuisines'] = df['cuisines'].apply(lambda x: x.split(','))

    df['menu_item'] = df['menu_item'].apply(ast.literal_eval)
    df['dishes'] = df['dish_liked'] + df['menu_item']
    df['dishes'] = df['dishes'].apply(lambda x: list(set(x)))

    return df
