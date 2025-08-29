from dash import Dash, dcc
import dash_mantine_components as dmc
import plotly.express as px
import pandas as pd

# Graph 1
df_2 = pd.read_csv("data/data_mmda_traffic_spatial.csv")
df_clean = df_2.dropna(subset=["Type"])
df_counts = (
    df_2.groupby(["Latitude", "Longitude"])
    .size()
    .reset_index(name="count")
)
df_counts = df_counts[~((df_counts["Latitude"] == 0) & (df_counts["Longitude"] == 0))]
fig_2 = px.scatter_map(
    df_counts,
    lat="Latitude",
    lon="Longitude",
    size="count",
    color="count",
    hover_data=["count"],
    zoom=10,
    height=600,
    map_style="carto-darkmatter",
    color_continuous_scale="Peach"
)

fig_2.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
fig_2.update_coloraxes(
    colorbar=dict(
        x=0.95,
        y=0.5,
        xanchor="left",
        yanchor="middle",
        len=0.6,
    )
)


# Graph 2
df = pd.read_csv("data/main.csv")
df['Count'] = pd.to_numeric(df['Count'], downcast='integer', errors='coerce')

df_area = df[(df["Vehicle_Type"] != "Total") & (df["Location"].str.contains("EDSA", case=False))]

fig = px.area(
    df_area,
    x="Year",
    y="Count",
    color="Vehicle_Type",
    line_group="Vehicle_Type",
    title="Traffic Composition by Vehicle Type (2012–2024)",
    labels={"Count": "Traffic Count", "Year": "Year"},
    height=600
)

# Styling
fig.update_layout(
    template="plotly_dark",
    title_font=dict(size=22, color="white"),
    xaxis=dict(title="Year", tickfont=dict(color="white")),
    yaxis=dict(title="Traffic Count", tickfont=dict(color="white")),
    legend=dict(title="Vehicle Type", font=dict(color="white"))
)


app = Dash(__name__)
server = app.server

app.layout = dmc.MantineProvider(
    theme={
        "colors": {"custom": ["#1E1E2F"]},     # define your custom color
        "primaryColor": "custom",
        "fontFamily": "Segoe UI, sans-serif"
    },
    children=dmc.Container(
        size="xl",
        p="xl",
        children=[
            dmc.SimpleGrid(
                cols=2,
                spacing="xl",
                verticalSpacing="xl",
                mt="128px",
                children=[
                    dmc.Stack(
                        gap="s",
                        children=[
                            dmc.Title(
                                children=[
                                    dmc.Text("manila, traffic!", span=True, c="#9E770C", inherit=True)
                                ],
                                size="54px"
                            ),
                            dmc.Text(
                                children=[
                                    dmc.Text("Exploring the traffic in manila, specifically in EDSA. The data is extracted from MMDA’s annual average daily traffic. Due to X’s API limitation, I’m unable to extract tweets from MMDAs twitter but fortunately, there was an existing dataset that covered the tweets from 2018 to 2020.", lh=1.2)
                                ],
                                size="20px",
                                ta="justify",
                                c="#565555"
                            )
                        ]
                    ),
                    dmc.Center()
                ]
            ),

            dmc.Space(h=250),
            dmc.Title(
                children=[
                    dmc.Text("manila traffic incidents from 2018 to 2020.", span=True, c="#9E770C", inherit=True)
                ],
                ml="15px",
                size="32px"
            ),
            dmc.Paper(
                withBorder=False,
                p="md",
                children=dcc.Graph(
                    figure=fig_2,
                    style={"width": "100%", "height": "500px"}
                )
            ),
            dmc.Space(h=100),
            dmc.Container(
                size=700,
                style={"marginLeft": 0, "marginRight": "auto"},
                children=[
                    dmc.Text(
                        children=[
                            dmc.Text("This is the visualization from the Kaggle dataset using Plotly Express. It shows that the traffic incidents "
                            "in C:4 (EDSA) is significantly higher than other circumferential and radial roads. The high volume of vehicles " \
                            "can also play a role in these traffic accidents. R:7 (Quezon Avenue and Commonwealth Avenue) and C:5 (C.P. Garcia / " \
                            "Katipunan Avenue / Tandang Sora) also shows a high number of traffic accidents. ", lh=1.2)
                        ],
                        size="22px",
                        ta="justify",
                        c="#565555"
                    )                    
                ]
            ),

            
            dmc.Space(h=200),

            # EDSA as the busiest road.
            dmc.Title(
                children=[
                    dmc.Text("top five roads 2012 and 2024", span=True, c="#9E770C", inherit=True)
                ],
                size="32px"),
            dmc.Grid(
                mt=20,
                children=[
                    dmc.GridCol(dmc.Box(
                        children=[
                            dmc.Stack(
                                children=[
                                    dmc.Image(
                                        h=300,
                                        src="/assets/2012_graph.png"
                                    ),
                                    dmc.Image(
                                        h=300,
                                        src="/assets/2024_graph.png"
                                    )
                                ]
                            )
                        ]
                    ), span=8),
                    dmc.GridCol(dmc.Box(
                        children=[
                            dmc.Text(
                                children=["This is the visualization from the MMDAs annual average daily traffic. I compiled all of the PDFs then merged it into a single dataset to visualize it using Plotly Express."], lh=1.2, size="22px", ta="justify", c="#565555"
                            ),
                            dmc.Space(h=50),
                            dmc.Text(
                                children=["In these bar graphs, C:4 or EDSA maintained the status of being the most abused road even after 12 years. It is then followed by Commonwealth Avenue, a part of R:7, which also shows a high amount of traffic accidents. C:5 also maintained being in the top 5."], lh=1.2, size="22px", ta="justify", c="#565555"
                            )
                        ]
                    ), span=4)
                ]
            ),

            dmc.Space(h=200),

            # Vehicles dominating the EDSA
            dmc.Title(
                children=[
                    dmc.Text("vehicles dominating the EDSA", span=True, c="#9E770C", inherit=True)
                ],
                size="32px"),
            dmc.Grid(
                mt=20,
                children=[
                    dmc.GridCol(
                            dmc.Paper(
                            withBorder=False,
                            children=dcc.Graph(
                            figure=fig,
                            style={"width": "100%", "height": "500px"}
                            )
                        ), span=9),
                    dmc.GridCol(dmc.Box(""), span=3)
                ]
            ),
            dmc.Text(
                mt=30,
                children=["Comparing the data from 2012 and 2024, we can see that the count of vehicles decreased over time while there was a “boom” in motorcycles. Cars, public utility jeepneys, public utility buses, and taxis decreased over time. While the daily count of motorcycles started from 38000 in 2012, the daily count of motorcycles now in EDSA is 189000. A whooping 397% increase."], lh=1.2, size="22px", ta="justify", c="#565555"
            ),

            dmc.Space(h=500),

            # Image
            dmc.Center(
                p="38px",
                style={"height": 200, "width": "100%"},
                children=[
                    dmc.Image(
                        h=250,
                        src="assets/image_5.png"
                    )
                ]
            ),

            dmc.Space(h=50),

            dmc.Text(
                children=["Is the sheer volume of vehicles the real culprit behind the gridlock in this hot, chaotic lane? According to the Metropolitan Manila Development Authority (MMDA), over 400,000 vehicles passed through it daily in 2023—far beyond its designed capacity of 300,000."], lh=1.2, size="22px", ta="justify", c="#565555"
            ),

            dmc.Text(
                mt=20,
                children=["Yet, despite the presence of the MRT, congestion remains relentless—and the MRT itself struggles with overcrowding and inefficiencies. Some point to weak urban planning across Metro Manila, while others highlight the overwhelming rise in private vehicle ownership. In reality, the crisis is not caused by a single factor but by a tangled web of infrastructure limits, policy shortcomings, and the daily choices of millions of commuters."], lh=1.2, size="22px", ta="justify", c="#565555"
            ),



        ]
    )
)

if __name__ == '__main__':

    app.run(debug=True)
