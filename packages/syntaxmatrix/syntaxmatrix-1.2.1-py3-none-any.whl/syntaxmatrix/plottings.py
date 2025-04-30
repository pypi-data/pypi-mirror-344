
import io
import base64

# Matplotlib Integration (Static Images)
def figure(*args, **kwargs):
    import matplotlib.pyplot as plt
    return plt.figure(*args, **kwargs)

def pyplot(fig, dpi=200):
    buf = io.BytesIO()
    fig.savefig(buf, format='png', bbox_inches='tight', dpi=dpi)
    buf.seek(0)
    img_data = base64.b64encode(buf.read()).decode('utf-8')
    html = f'<img src="data:image/png;base64,{img_data}" style="max-width:100%;">'
    return html

# Plotly Integration (Interactive, Hover Tooltips)
def plotly():
    import plotly.express as px
    return px

def render_plotly(fig):
    html = fig.to_html(
        full_html=False,
        include_plotlyjs='cdn',
        config={"displaylogo": False}
    )
    return html
