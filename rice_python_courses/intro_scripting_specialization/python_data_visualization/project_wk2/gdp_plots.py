"""
Project for Week 2 of "Python Data Visualization".
Read World Bank GDP data and create some basic XY plots.

Be sure to read the project description page for further information
about the expected behavior of the program.
"""

import csv
import pygal


def read_csv_as_nested_dict(filename, keyfield, separator, quote):
    """
    Inputs:
      filename  - name of CSV file
      keyfield  - field to use as key for rows
      separator - character that separates fields
      quote     - character used to optionally quote fields
    Output:
      Returns a dictionary of dictionaries where the outer dictionary
      maps the value in the key_field to the corresponding row in the
      CSV file.  The inner dictionaries map the field names to the
      field values for that row.
    """
    table = {}
    with open(filename, "rt", newline='') as csvfile:
        csv_reader = csv.DictReader(csvfile,
                                    delimiter=separator,
                                    quotechar=quote)
        for row in csv_reader:
            table[row[keyfield]] = row
    return table


def build_plot_values(gdpinfo, gdpdata):
    """
    Inputs:
      gdpinfo - GDP data information dictionary
      gdpdata - A single country's GDP stored in a dictionary whose
                keys are strings indicating a year and whose values
                are strings indicating the country's corresponding GDP
                for that year.

    Output: 
      Returns a list of tuples of the form (year, GDP) for the years
      between "min_year" and "max_year", inclusive, from gdpinfo that
      exist in gdpdata.  The year will be an integer and the GDP will
      be a float.
    """
    x_min = gdpinfo["min_year"]
    x_max = gdpinfo["max_year"]
    gdp_by_year = []
    for key in gdpdata:
        try:
            year = int(key)
        except ValueError:
            continue
        if year < x_min or year > x_max:
            continue

        try:
            gdp_that_year = float(gdpdata[key])
        except ValueError:
            continue
        gdp_by_year.append((year, gdp_that_year))
    gdp_by_year.sort()
    return gdp_by_year


def build_plot_dict(gdpinfo, country_list):
    """
    Inputs:
      gdpinfo      - GDP data information dictionary
      country_list - List of strings that are country names

    Output:
      Returns a dictionary whose keys are the country names in
      country_list and whose values are lists of XY plot values 
      computed from the CSV file described by gdpinfo.

      Countries from country_list that do not appear in the
      CSV file should still be in the output dictionary, but
      with an empty XY plot value list.
    """
    gdp_data = read_csv_as_nested_dict(gdpinfo["gdpfile"],
                                       gdpinfo["country_name"],
                                       gdpinfo["separator"],
                                       gdpinfo["quote"])
    gdp_sel = {}
    for ctry in country_list:
        ct_dict = gdp_data.get(ctry, None)
        gdp_sel[ctry] = build_plot_values(gdpinfo, ct_dict) if ct_dict is not None else []
    return gdp_sel


def render_xy_plot(gdpinfo, country_list, plot_file):
    """
    Inputs:
      gdpinfo      - GDP data information dictionary
      country_list - List of strings that are country names
      plot_file    - String that is the output plot file name

    Output:
      Returns None.

    Action:
      Creates an SVG image of an XY plot for the GDP data
      specified by gdpinfo for the countries in country_list.
      The image will be stored in a file named by plot_file.
    """
    gdp_sel = build_plot_dict(gdpinfo, country_list)
    xy_chart = pygal.XY(title='GDP Data', x_title='Year', y_title='Current US[$]')
    for country in country_list:
        xy_chart.add(country, gdp_sel[country])
    xy_chart.render_to_file(plot_file)


def test_render_xy_plot():
    """
    Code to exercise render_xy_plot and generate plots from
    actual GDP data.
    """
    gdpinfo = {
        "gdpfile": "isp_gdp.csv",
        "separator": ",",
        "quote": '"',
        "min_year": 1960,
        "max_year": 2015,
        "country_name": "Country Name",
        "country_code": "Country Code"
    }

    render_xy_plot(gdpinfo, [], "isp_gdp_xy_none.svg")
    render_xy_plot(gdpinfo, ["China"], "isp_gdp_xy_china.svg")
    render_xy_plot(gdpinfo, ["United Kingdom", "United States"],
                   "isp_gdp_xy_uk+usa.svg")

# Make sure the following call to test_render_xy_plot is commented out
# when submitting to OwlTest/CourseraTest.

# test_render_xy_plot()
