from sysnarrator.widgets.charts import sparkline_string, BrailleAreaChart

def test_sparkline_generation():
    vals = [0.0, 25.0, 50.0, 75.0, 100.0]
    spark = sparkline_string(vals, width=5)
    assert len(spark) == 5
    assert spark[0] == " "
    assert spark[-1] == "█"

def test_braille_chart_widget_initialization():
    chart = BrailleAreaChart(title="CPU Load", min_val=0.0, max_val=100.0, color_scheme="thermal")
    chart.data = [10.0, 20.0, 50.0, 80.0, 95.0]
    assert chart.title == "CPU Load"
    assert len(chart.data) == 5
