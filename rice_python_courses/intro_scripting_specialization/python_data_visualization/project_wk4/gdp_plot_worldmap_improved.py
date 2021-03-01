"""
Project for Week 4 of "Python Data Visualization".
Unify data via common country codes.

Be sure to read the project description page for further information
about the expected behavior of the program.
"""

import csv
import math
import pygal


def build_country_code_converter(codeinfo):
    """
    Inputs:
      codeinfo      - A country code information dictionary

    Output:
      A dictionary whose keys are plot country codes and values
      are world bank country codes, where the code fields in the
      code file are specified in codeinfo.
    """
    country_code_ref_dict = {}

    country_codes = read_csv_as_nested_dict(codeinfo["codefile"],
                                            codeinfo["plot_codes"],
                                            codeinfo["separator"],
                                            codeinfo["quote"])
    for code in country_codes:
        country_code_ref_dict[code] = country_codes[code].get(codeinfo["data_codes"])
    return country_code_ref_dict


def reconcile_countries_by_code(codeinfo, plot_countries, gdp_countries):
    """
    Inputs:
      codeinfo       - A country code information dictionary
      plot_countries - Dictionary whose keys are plot library country codes
                       and values are the corresponding country name
      gdp_countries  - Dictionary whose keys are country codes used in GDP data

    Output:
      A tuple containing a dictionary and a set.  The dictionary maps
      country codes from plot_countries to country codes from
      gdp_countries.  The set contains the country codes from
      plot_countries that did not have a country with a corresponding
      code in gdp_countries.

      Note that all codes should be compared in a case-insensitive
      way.  However, the returned dictionary and set should include
      the codes with the exact same case as they have in
      plot_countries and gdp_countries.
    """
    # keys are two letter codes and values are three letter codes
    country_code_ref_dict = build_country_code_converter(codeinfo)
    plot_bank_map = {}
    unknown_countries = set()

    code_converter_ref = {code2.casefold(): code3.casefold()
                          for code2, code3 in country_code_ref_dict.items()}
    plot_codes = {code.casefold(): code for code in plot_countries.keys()}
    gdp_countries_codes = {code.casefold(): code for code in gdp_countries.keys()}

    for code in plot_codes:
        if code in code_converter_ref:
            gdp_code = code_converter_ref.get(code)
            if gdp_code in gdp_countries_codes:
                plot_bank_map[plot_codes.get(code)] = gdp_countries_codes.get(gdp_code)
            else:
                unknown_countries.add(plot_codes.get(code))
        else:
            unknown_countries.add(plot_codes.get(code))
    return plot_bank_map, unknown_countries


def build_map_dict_by_code(gdpinfo, codeinfo, plot_countries, year):
    """
    Inputs:
      gdpinfo        - A GDP information dictionary
      codeinfo       - A country code information dictionary
      plot_countries - Dictionary mapping plot library country codes to country names
      year           - String year for which to create GDP mapping

    Output:
      A tuple containing a dictionary and two sets.  The dictionary
      maps country codes from plot_countries to the log (base 10) of
      the GDP value for that country in the specified year.  The first
      set contains the country codes from plot_countries that were not
      found in the GDP data file.  The second set contains the country
      codes from plot_countries that were found in the GDP data file, but
      have no GDP data for the specified year.
    """
    gdp_data = read_csv_as_nested_dict(gdpinfo["gdpfile"],
                                       gdpinfo["country_code"],
                                       gdpinfo["separator"],
                                       gdpinfo["quote"])

    common, unknown = reconcile_countries_by_code(codeinfo, plot_countries, gdp_data)
    gdp_countries = dict()
    gdp_unknown = set()

    if int(year) < gdpinfo["min_year"] or int(year) > gdpinfo["max_year"]:
        return {}, unknown, set(common.keys())

    for ct_code in common:
        try:
            gdp = float(gdp_data[common.get(ct_code)].get(year))
            gdp_countries[ct_code] = math.log10(gdp)
        except ValueError:
            gdp_unknown.add(ct_code)
    return gdp_countries, unknown, gdp_unknown


def render_world_map(gdpinfo, codeinfo, plot_countries, year, map_file):
    """
    Inputs:
      gdpinfo        - A GDP information dictionary
      codeinfo       - A country code information dictionary
      plot_countries - Dictionary mapping plot library country codes to country names
      year           - String year of data
      map_file       - String that is the output map file name

    Output:
      Returns None.

    Action:
      Creates a world map plot of the GDP data in gdp_mapping and outputs
      it to a file named by svg_filename.
    """
    chart_title = "GDP by country for {} (log scale), unified by common country NAME"
    chart_title = chart_title.format(year)

    legend1 = "GDP for {}".format(year)
    legend2 = "Missing from World Bank Data"
    legend3 = "No GDP data"

    worldmap_chart = pygal.maps.world.World()
    worldmap_chart.title = chart_title

    gdp_dict, missing_set, no_gdp_set = build_map_dict_by_code(gdpinfo, codeinfo,
                                                               plot_countries, year)

    worldmap_chart.add(legend1, gdp_dict)
    worldmap_chart.add(legend2, list(missing_set))
    worldmap_chart.add(legend3, list(no_gdp_set))
    worldmap_chart.render_to_file(map_file)


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


def test_render_world_map():
    """
    Test the project code for several years
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

    codeinfo = {
        "codefile": "isp_country_codes.csv",
        "separator": ",",
        "quote": '"',
        "plot_codes": "ISO3166-1-Alpha-2",
        "data_codes": "ISO3166-1-Alpha-3"
    }

    # Get pygal country code map
    pygal_countries = pygal.maps.world.COUNTRIES

    # 1960
    render_world_map(gdpinfo, codeinfo, pygal_countries, "1960", "isp_gdp_world_code_1960.svg")

    # 1980
    render_world_map(gdpinfo, codeinfo, pygal_countries, "1980", "isp_gdp_world_code_1980.svg")

    # 2000
    render_world_map(gdpinfo, codeinfo, pygal_countries, "2000", "isp_gdp_world_code_2000.svg")

    # 2010
    render_world_map(gdpinfo, codeinfo, pygal_countries, "2010", "isp_gdp_world_code_2010.svg")


# Make sure the following call to test_render_world_map is commented
# out when submitting to OwlTest/CourseraTest.

# test_render_world_map()
