import os
import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import io

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)

st.set_page_config(
    page_title="Creative Intelligence AI",
    page_icon="🎨",
    layout="wide"
)

BACKEND_URL = os.getenv(
    "BACKEND_URL",
    "https://creative-intelligence-ai-api.onrender.com"
).rstrip("/")

API_URL = f"{BACKEND_URL}/upload-image"

st.title("🎨 Creative Intelligence AI")
st.subheader("AI-Powered Advertisement Analysis Platform")

st.markdown(
    "Analyze advertisement designs using Computer Vision and AI."
)

st.divider()

st.header("📤 Upload Advertisement")

uploaded_file = st.file_uploader(
    "Choose an advertisement image",
    type=["jpg", "jpeg", "png", "webp"]
)

if uploaded_file is not None:

    st.image(
        uploaded_file,
        caption="Uploaded Advertisement",
        use_container_width=True
    )

    if st.button("Analyze Advertisement", type="primary"):

        with st.spinner("Analyzing advertisement..."):

            try:
                files = {
                    "file": (
                        uploaded_file.name,
                        uploaded_file.getvalue(),
                        uploaded_file.type
                    )
                }

                response = requests.post(
                    API_URL,
                    files=files,
                    timeout=120
                )

                if response.status_code == 200:

                    result = response.json()
                    analysis = result["analysis"]

                    st.session_state["analysis_result"] = result

                else:
                    try:
                        error_message = response.json().get(
                            "detail",
                            "Something went wrong."
                        )
                    except ValueError:
                        error_message = "Invalid backend response."

                    st.error(error_message)

            except requests.exceptions.ConnectionError:
                st.error(
                    "Backend connection failed. "
                    "Please start the FastAPI server."
                )

            except requests.exceptions.Timeout:
                st.error("Analysis timed out. Please try again.")

            except requests.exceptions.RequestException as error:
                st.error(f"API request failed: {error}")


if "analysis_result" in st.session_state:

    result = st.session_state["analysis_result"]
    analysis = result["analysis"]

    st.success("Advertisement analyzed successfully!")

    st.divider()
    st.header("📊 Design Intelligence Dashboard")

    st.subheader("🎨 Design Quality Scores")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Brightness Score",
        f"{analysis['Brightness Score']:.2f}"
    )

    col2.metric(
        "Contrast Score",
        f"{analysis['Contrast Score']:.2f}"
    )

    col3.metric(
        "Resolution Score",
        f"{analysis['Resolution Score']:.2f}"
    )

    col4, col5, col6 = st.columns(3)

    col4.metric(
        "Design Score",
        f"{analysis['Design Score']:.2f}"
    )

    col5.metric(
        "Colour Diversity",
        f"{analysis['Colour Diversity Score']:.2f}"
    )

    col6.metric(
        "Updated Design Score",
        f"{analysis['Updated Design Score']:.2f}"
    )

    st.divider()
    st.subheader("👁️ Visual Attention Analysis")

    col7, col8, col9 = st.columns(3)

    col7.metric(
        "Average Saliency",
        f"{analysis['Average Saliency Score']:.2f}"
    )

    col8.metric(
        "Maximum Saliency",
        f"{analysis['Maximum Saliency']:.4f}"
    )

    col9.metric(
        "Minimum Saliency",
        f"{analysis['Minimum Saliency']:.4f}"
    )

    saliency_data = pd.DataFrame({
        "Saliency Metric": [
            "Average Saliency",
            "Maximum Saliency",
            "Minimum Saliency"
        ],
        "Value": [
            analysis["Average Saliency Score"],
            analysis["Maximum Saliency"],
            analysis["Minimum Saliency"]
        ]
    })

    saliency_fig = px.bar(
        saliency_data,
        x="Saliency Metric",
        y="Value",
        title="Visual Attention Statistics",
        text_auto=".4f"
    )

    st.plotly_chart(
        saliency_fig,
        use_container_width=True
    )

    st.caption(
        "Saliency values represent algorithmic visual saliency, "
        "not measured human eye-tracking."
    )

    st.divider()
    st.subheader("📁 Image Information")

    st.write("Filename:", result["filename"])
    st.write("Width:", result["image_width"], "pixels")
    st.write("Height:", result["image_height"], "pixels")
    st.write("File Size:", result["file_size"], "bytes")

    st.divider()
    st.subheader("📈 Design Score Visualization")

    score_data = pd.DataFrame({
        "Metric": [
            "Brightness",
            "Contrast",
            "Resolution",
            "Design",
            "Colour Diversity",
            "Updated Design"
        ],
        "Score": [
            analysis["Brightness Score"],
            analysis["Contrast Score"],
            analysis["Resolution Score"],
            analysis["Design Score"],
            analysis["Colour Diversity Score"],
            analysis["Updated Design Score"]
        ]
    })

    fig = px.bar(
        score_data,
        x="Metric",
        y="Score",
        title="Advertisement Design Intelligence Scores",
        range_y=[0, 100],
        text_auto=".2f"
    )

    fig.update_layout(
        yaxis_title="Score (0–100)",
        xaxis_title="Design Metrics"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.divider()
    st.subheader("🌈 Colour Diversity Analysis")

    colour_score = analysis["Colour Diversity Score"]

    colour_data = pd.DataFrame({
        "Category": [
            "Colour Diversity",
            "Remaining Score"
        ],
        "Value": [
            colour_score,
            max(0, 100 - colour_score)
        ]
    })

    colour_fig = px.pie(
        colour_data,
        names="Category",
        values="Value",
        title="Colour Diversity Score Distribution",
        hole=0.55
    )

    st.plotly_chart(
        colour_fig,
        use_container_width=True
    )

    st.divider()
    st.header("📝 Advertisement Analysis Summary")

    design_score = analysis["Updated Design Score"]
    brightness = analysis["Brightness Score"]
    contrast = analysis["Contrast Score"]
    diversity = analysis["Colour Diversity Score"]

    st.metric(
        "Overall Updated Design Score",
        f"{design_score:.2f}/100"
    )

    if design_score >= 80:
        st.success(
            "The advertisement has a high score "
            "under the current design scoring method."
        )
    elif design_score >= 60:
        st.info(
            "The advertisement has a moderate score "
            "under the current design scoring method."
        )
    else:
        st.warning(
            "The advertisement has a lower score "
            "under the current design scoring method."
        )

    st.write("**Visual observations:**")

    if brightness < 50:
        st.write("- The image has relatively low brightness.")
    elif brightness > 80:
        st.write("- The image has relatively high brightness.")
    else:
        st.write("- Brightness falls in the middle range.")

    if contrast < 50:
        st.write("- The image has relatively low contrast.")
    else:
        st.write("- The image has relatively high contrast.")

    st.write(
        f"- Colour diversity score: {diversity:.2f}/100."
    )

    st.caption(
        "These are heuristic observations based on image statistics, "
        "not guaranteed advertising performance or conversion predictions."
    )

    report_data = {
        "Filename": result["filename"],
        "Image Width": result["image_width"],
        "Image Height": result["image_height"],
        "File Size": result["file_size"],
        **analysis
    }

    report_df = pd.DataFrame([report_data])

    st.divider()
    st.header("⬇️ Download Analysis Reports")

    csv_report = report_df.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        label="📄 Download CSV Report",
        data=csv_report,
        file_name="creative_intelligence_report.csv",
        mime="text/csv"
    )

    pdf_buffer = io.BytesIO()

    pdf_doc = SimpleDocTemplate(
        pdf_buffer,
        pagesize=A4,
        rightMargin=0.6 * inch,
        leftMargin=0.6 * inch,
        topMargin=0.6 * inch,
        bottomMargin=0.6 * inch
    )

    styles = getSampleStyleSheet()

    story = []

    story.append(
        Paragraph(
            "Creative Intelligence AI",
            styles["Title"]
        )
    )

    story.append(
        Paragraph(
            "Advertisement Design Analysis Report",
            styles["Heading2"]
        )
    )

    story.append(Spacer(1, 20))

    story.append(
        Paragraph(
            f"Filename: {result['filename']}",
            styles["Normal"]
        )
    )

    story.append(
        Paragraph(
            f"Image Dimensions: {result['image_width']} x "
            f"{result['image_height']} pixels",
            styles["Normal"]
        )
    )

    story.append(Spacer(1, 20))

    story.append(
        Paragraph(
            "Design Intelligence Metrics",
            styles["Heading2"]
        )
    )

    table_data = [["Metric", "Score"]]

    for metric, value in analysis.items():
        table_data.append([
            metric,
            f"{value:.4f}"
        ])

    metrics_table = Table(
        table_data,
        colWidths=[3.5 * inch, 2 * inch]
    )

    metrics_table.setStyle(
        TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#243B53")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("PADDING", (0, 0), (-1, -1), 8),
            ("ALIGN", (1, 1), (1, -1), "CENTER"),
        ])
    )

    story.append(metrics_table)

    story.append(Spacer(1, 20))

    story.append(
        Paragraph(
            "Overall Updated Design Score",
            styles["Heading2"]
        )
    )

    story.append(
        Paragraph(
            f"{design_score:.2f}/100",
            styles["Title"]
        )
    )

    story.append(Spacer(1, 15))

    story.append(
        Paragraph(
            "Note: Scores are based on the project's current "
            "heuristic computer vision analysis. They do not "
            "guarantee real-world advertising performance.",
            styles["Italic"]
        )
    )

    pdf_doc.build(story)

    pdf_report = pdf_buffer.getvalue()

    st.download_button(
        label="📕 Download PDF Report",
        data=pdf_report,
        file_name="creative_intelligence_report.pdf",
        mime="application/pdf"
    )
