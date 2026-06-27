import pandas as pd
import plotly.express as px

def chart(data: pd.DataFrame, year: int, top_n: int):
    snapshot = data[data["year"] == year]

    group_sector = snapshot.groupby(["Name", "sector"]).sum().reset_index()
    top_countries = group_sector.groupby("Name")["co2"].sum().sort_values(ascending=False).head(top_n).index.tolist()
    print("Top countries: ", top_countries) # DEBUG

    top_sectors = group_sector.groupby("sector")["co2"].sum().sort_values(ascending=False).head(9).index.tolist()
    print("Top sectors: ", top_sectors)

    group_sector["sector"] = group_sector["sector"].where(
        group_sector["sector"].isin(top_sectors), other="Other"
    )
    print("Group sectors: ", group_sector) # DEBUG

    plot_data = group_sector[group_sector["Name"].isin(top_countries)]
    print("Plot data: ", plot_data) # DEBUG

    fig = px.bar(
        plot_data,
        x="co2",
        y="Name",
        labels={"co2": "CO₂ (million tonnes)", "Name": ""},
        color="sector",
        barmode="stack",
        color_discrete_map={"Other": "lightgray"},
        category_orders={"Name": top_countries, "sector": top_sectors + ["Other"]},
    )

    fig.update_layout(
        xaxis=dict(showgrid=True),
        yaxis=dict(autorange="reversed", tickfont=dict(size=16), showgrid=True)
    )

    return fig
