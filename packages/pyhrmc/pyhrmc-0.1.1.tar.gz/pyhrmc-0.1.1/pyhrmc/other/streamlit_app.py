# streamlit_app.py
import streamlit as st
import pandas as pd
import plotly.express as px  
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import time

class treamlit_app():
    def __init__(self,plot_E = True, plot_T = True, plot_unc = False):
        self.data_file ="/media/synology/user/karen/flare/large_al2o3/correction2/3.3_1000_05_16_5/error_plotting.txt"
        self.pdf_file = "/media/synology/user/karen/flare/large_al2o3/correction2/3.3_1000_05_16_5/pdf.txt"
        self.ref_pdf = "/media/synology/user/karen/flare/large_al2o3/correction2/3.3_1000_05_16_5/al2o3_5nm_gr.txt"
        self.plot_E = plot_E
        self.plot_T = plot_T
        self.plot_unc = plot_unc

    def get_data(self) -> pd.DataFrame:
        return pd.read_csv(self.data_file,delim_whitespace=True, header=None)
    
    def get_pdf(self):
        """Reads x and y data from the additional text file."""
        with open(self.pdf_file, "r") as file:
            lines = file.readlines()
            r_values = list(map(float, lines[0].strip().split()))
            Gr_values = list(map(float, lines[1].strip().split()))


        # Load the data file, assuming it's space or comma-delimited
        data = pd.read_csv(self.ref_pdf, sep=",", header=None)
        # Split into x and y values
        ref_r = data[0]  # First column
        ref_Gr = data[1]  # Second column

        return r_values, Gr_values, ref_r, ref_Gr

    def run_streamlit_app(self):
        df = self.get_data()
        #BUG: REMOVE HARDCODING
        df.columns = ["Step_number", "MSE", "Energy (eV/atom)", "Sigma", "Temperature (K)", "Unused"]

        st.set_page_config(
            page_title="pyHRMC Simulation Progress",
            page_icon=":chart_with_downwards_trend:",
            layout="wide",
        )
        # dashboard title
        st.title("pyHRMC Progress Dashboard :sparkles:")

        # creating a single-element container.
        placeholder = st.empty()
        with placeholder.container():
            r_values, Gr_values, ref_r, ref_Gr = self.get_pdf()
            left_co, cent_co,last_co = st.columns(3)
            with cent_co:
                fig0 = go.Figure()
                
                fig0.add_trace(go.Scatter(
                    x=r_values,
                    y=Gr_values,
                    mode="lines",
                    name="G(r) calculated"
                ))
                fig0.add_trace(go.Scatter(
                    x=ref_r,
                    y=ref_Gr,
                    mode="lines",
                    name="G(r) experimental"
                ))

                fig0.update_layout(
                    width=800,
                    title=dict(
                        text="PDF plot",
                        font=dict(size=24, color="black")
                        ),
                    xaxis_title=dict(
                        text="r (Angstroms)",
                        font=dict(size=18, color="black")
                        ),
                    yaxis_title=dict(
                        text="G(r)",
                        font=dict(size=18, color="black")
                        )
                )
                fig0.update_xaxes(tickfont=dict(size=18, color="black"))
                fig0.update_yaxes(tickfont=dict(size=18, color="black"))
                st.write(fig0)

            # create two columns for charts
            left_co, col1, col2, right_co = st.columns([1,2,2,1], gap="large")

            with col1:
                fig = px.line(
                    data_frame=df, y="MSE", x="Step_number"
                )
                fig.update_layout(
                    width=800,
                    title=dict(
                        text="MSE over Simulation Steps",
                        font=dict(size=24, color="black")
                        ),
                    xaxis_title=dict(
                        text="Step Number",
                        font=dict(size=18, color="black")
                        ),
                    yaxis_title=dict(
                        text="Mean Squared Error (MSE)",
                        font=dict(size=18, color="black")
                        )
                )
                fig.update_xaxes(tickfont=dict(size=18, color="black"))
                fig.update_yaxes(tickfont=dict(size=18, color="black"))
                st.write(fig)

            with col2:
                fig2 = px.line(
                    data_frame=df, y="Sigma", x="Step_number"
                )
                fig2.update_layout(
                    width=800,
                    title=dict(
                        text="Sigma over Simulation Steps",
                        font=dict(size=24, color="black")
                        ),
                    xaxis_title=dict(
                        text="Step Number",
                        font=dict(size=18, color="black")
                        ),
                    yaxis_title=dict(
                        text="Sigma",
                        font=dict(size=18, color="black")
                        )
                )
                fig2.update_xaxes(tickfont=dict(size=18, color="black"))
                fig2.update_yaxes(tickfont=dict(size=18, color="black"))
                st.write(fig2)


            left_co, col3, col4, right_co = st.columns([1,2,2, 1], gap="large")

            if self.plot_E:
                with col3:
                    fig3 = px.line(
                        data_frame=df, y="Energy (eV/atom)", x="Step_number"
                    )
                    fig3.update_layout(
                        width=800,
                        title=dict(
                            text="Energy over Simulation Steps",
                            font=dict(size=24, color="black")
                            ),
                        xaxis_title=dict(text="Step Number",font=dict(size=18, color="black")),
                        yaxis_title=dict(text="Energy (eV/atom)",font=dict(size=18, color="black"))
                    )
                    fig3.update_xaxes(tickfont=dict(size=18, color="black"))
                    fig3.update_yaxes(tickfont=dict(size=18, color="black"))
                    st.write(fig3)

            if self.plot_T:
                with col4:
                    fig4 = px.line(
                        data_frame=df, y="Temperature (K)", x="Step_number"
                    )
                    fig4.update_layout(
                        width=800,
                        title=dict(text="Temperature over Simulation Steps",font=dict(size=24, color="black")),
                        xaxis_title=dict(text="Step Number",font=dict(size=18, color="black")),
                        yaxis_title=dict(text="Temperature (K)",font=dict(size=18, color="black"))
                    )
                    fig4.update_xaxes(tickfont=dict(size=18, color="black"))
                    fig4.update_yaxes(tickfont=dict(size=18, color="black"))
                    st.write(fig4)

        # Refresh periodically
        time.sleep(300)  # Sleep for 5 seconds
        st.rerun()

        # Run the Streamlit app
app = streamlit_app()
app.run_streamlit_app()