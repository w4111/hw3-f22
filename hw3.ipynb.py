{
  "cells": [
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "J1qjQ6cW_z8d"
      },
      "source": [
        "# Homework 3\n",
        "\n",
        "* Assigned: 10/13\n",
        "\n",
        "* Due: 11/1 @ 11:59PM ET on Gradescope\n",
        "\n",
        "* Value: 3.75% of your grade\n",
        "\n",
        "In this assignment it's time to get real! You'll first flex your SQL muscles and perform analyses similar to HW2's by writing SQL and reflecting on the experience. You will then perform some normalization."
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "4cd6fsKLtv4o"
      },
      "source": [
        "# Assignment description\n",
        "\n",
        "In this assignment, you will be performing more complex analysis using the full iowa dataset.   In contrast to when we directly wrote SQL queries using the magic `%%sql` cells, we will be directly connecting to the database and running queries through the Python database client.   This is how the magic `%%sql` cells are implemented under the covers anyways.\n",
        "\n",
        "We will also be using [DuckDB](https://duckdb.org/), a new database system designed for analytics.  It is very similar to the SQLite database we have used in the past, however it is _must faster_ when analyzing the entire dataset."
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "KbAJTKAotv4p"
      },
      "source": [
        "# Setup code \n",
        "The following three blocks only need to run once.   It will install duckdb, download the data files, and load it into duckdb.\n",
        "\n"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 3,
      "metadata": {
        "id": "gfcloLcF_z8i",
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "outputId": "b07d146f-b549-4f80-e37a-8f1c02a4e9ce"
      },
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "Looking in indexes: https://pypi.org/simple, https://us-python.pkg.dev/colab-wheels/public/simple/\n",
            "Collecting duckdb\n",
            "  Downloading duckdb-0.5.1-cp37-cp37m-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (16.4 MB)\n",
            "\u001b[K     |████████████████████████████████| 16.4 MB 5.0 MB/s \n",
            "\u001b[?25hRequirement already satisfied: numpy>=1.14 in /usr/local/lib/python3.7/dist-packages (from duckdb) (1.21.6)\n",
            "Installing collected packages: duckdb\n",
            "Successfully installed duckdb-0.5.1\n",
            "rm: cannot remove 'iowa.csv*': No such file or directory\n",
            "rm: cannot remove 'iowa.duckdb*': No such file or directory\n",
            "--2022-10-13 21:45:56--  https://www.dropbox.com/s/0f4g8xa5m2s898i/iowa.csv\n",
            "Resolving www.dropbox.com (www.dropbox.com)... 162.125.5.18, 2620:100:601d:18::a27d:512\n",
            "Connecting to www.dropbox.com (www.dropbox.com)|162.125.5.18|:443... connected.\n",
            "HTTP request sent, awaiting response... 302 Found\n",
            "Location: /s/raw/0f4g8xa5m2s898i/iowa.csv [following]\n",
            "--2022-10-13 21:45:57--  https://www.dropbox.com/s/raw/0f4g8xa5m2s898i/iowa.csv\n",
            "Reusing existing connection to www.dropbox.com:443.\n",
            "HTTP request sent, awaiting response... 302 Found\n",
            "Location: https://uc2703a120da620d18036c9ea74e.dl.dropboxusercontent.com/cd/0/inline/Buzt2MvXz4Ov8QS94NBtIgvKKWaJznn650XB1xfGexEnEZIVpbthrC9yM8W0mLGfv95VeKBZ0zQ9D9XH6hClhRMxs_U_X4Td9FatRUhHSWa9VmwzwGrjd1HRxjRlDPZ-_rpCbSJVNsPMRS-cBA0r87kVzUyHRWdreXVoe4EhsI4REA/file# [following]\n",
            "--2022-10-13 21:45:57--  https://uc2703a120da620d18036c9ea74e.dl.dropboxusercontent.com/cd/0/inline/Buzt2MvXz4Ov8QS94NBtIgvKKWaJznn650XB1xfGexEnEZIVpbthrC9yM8W0mLGfv95VeKBZ0zQ9D9XH6hClhRMxs_U_X4Td9FatRUhHSWa9VmwzwGrjd1HRxjRlDPZ-_rpCbSJVNsPMRS-cBA0r87kVzUyHRWdreXVoe4EhsI4REA/file\n",
            "Resolving uc2703a120da620d18036c9ea74e.dl.dropboxusercontent.com (uc2703a120da620d18036c9ea74e.dl.dropboxusercontent.com)... 162.125.5.15, 2620:100:601b:15::a27d:80f\n",
            "Connecting to uc2703a120da620d18036c9ea74e.dl.dropboxusercontent.com (uc2703a120da620d18036c9ea74e.dl.dropboxusercontent.com)|162.125.5.15|:443... connected.\n",
            "HTTP request sent, awaiting response... 200 OK\n",
            "Length: 322749695 (308M) [text/plain]\n",
            "Saving to: ‘iowa.csv’\n",
            "\n",
            "iowa.csv            100%[===================>] 307.80M  99.1MB/s    in 3.1s    \n",
            "\n",
            "2022-10-13 21:46:01 (99.1 MB/s) - ‘iowa.csv’ saved [322749695/322749695]\n",
            "\n"
          ]
        }
      ],
      "source": [
        "!pip install duckdb\n",
        "!rm iowa.csv* iowa.duckdb*\n",
        "!wget https://www.dropbox.com/s/0f4g8xa5m2s898i/iowa.csv"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 4,
      "metadata": {
        "id": "70xAsiKs__ML"
      },
      "outputs": [],
      "source": [
        "import duckdb\n",
        "db = duckdb.connect('iowa.db')\n",
        "db.execute(\"CREATE TABLE iowa AS SELECT * FROM read_csv_auto('iowa.csv')\")\n",
        "\n",
        "def runq(q):\n",
        "  \"I'm helper function to run and print queries\"\n",
        "  cursor = db.execute(q)\n",
        "  df = cursor.fetchdf()\n",
        "  print(df)\n",
        "  return df\n"
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "HTxAqF9U_z8l"
      },
      "source": [
        "## Database Connection"
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "kgRTIulp_z8m"
      },
      "source": [
        "We are using a ~1M-tuple sample of the iowa liquor sales data for this assignment, with column names and datatype (in format of [name] [datatype]) as:\n",
        "\n",
        "  - address char(256),\n",
        "  - bottle_volume_ml integer,\n",
        "  - category char(256),\n",
        "  - category_name char(256),\n",
        "  - city char(256),\n",
        "  - county char(256),\n",
        "  - county_number char(256),\n",
        "  - date date,\n",
        "  - im_desc char(256),\n",
        "  - invoice_line_no char(256),\n",
        "  - itemno integer,\n",
        "  - name char(256),\n",
        "  - pack integer,\n",
        "  - sale_bottles integer,\n",
        "  - sale_dollars double precision,\n",
        "  - sale_gallons double precision,\n",
        "  - sale_liters double precision,\n",
        "  - state_bottle_cost double precision,\n",
        "  - state_bottle_retail double precision,\n",
        "  - store integer,\n",
        "  - store_location char(256),\n",
        "  - store_location_address char(256),\n",
        "  - store_location_city char(256),\n",
        "  - store_location_zip char(256),\n",
        "  - vendor_name char(256),\n",
        "  - vendor_no integer,\n",
        "  - zipcode text\n",
        "  \n",
        "A description of column names can be found here: https://data.iowa.gov/Economy/Iowa-Liquor-Sales/m3tr-qhgy."
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "JgFEq_fG_z8n"
      },
      "source": [
        "You may run this query to have some ideas on the schema you are dealing with:"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 6,
      "metadata": {
        "id": "jMHlVLqS_z8n",
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 1000
        },
        "outputId": "c373e145-be9b-4e3f-cd83-d9966c890790"
      },
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "  invoice_line_no       date  store                               name  \\\n",
            "0    S29198800001 2015-11-20   2191                     Keokuk Spirits   \n",
            "1    S29195400002 2015-11-21   2205             Ding's Honk And Holler   \n",
            "2    S29050300001 2015-11-16   3549               Quicker Liquor Store   \n",
            "3    S28867700001 2015-11-04   2513   Hy-Vee Food Store #2 / Iowa City   \n",
            "4    S29050800001 2015-11-17   3942                   Twin Town Liquor   \n",
            "5    S28869200001 2015-11-11   3650         Spirits, Stogies and Stuff   \n",
            "6    S28865700001 2015-11-09   2538    Hy-Vee Food Store #3 / Waterloo   \n",
            "7    S28869500001 2015-11-10   3942                   Twin Town Liquor   \n",
            "8    S29339300091 2015-11-30   2662  Hy-Vee Wine & Spirits / Muscatine   \n",
            "9    S29050900001 2015-11-16   4307         Crossroads Wine and Liquor   \n",
            "\n",
            "                 address          city zipcode  \\\n",
            "0              1013 MAIN        KEOKUK   52632   \n",
            "1       900 E WASHINGTON      CLARINDA   51632   \n",
            "2           1414 48TH ST  FORT MADISON   52627   \n",
            "3         812  S 1ST AVE     IOWA CITY   52240   \n",
            "4    104 HIGHWAY 30 WEST        TOLEDO   52342   \n",
            "5     118 South Main St.      HOLSTEIN   51025   \n",
            "6       1422 FLAMMANG DR      WATERLOO   50702   \n",
            "7    104 HIGHWAY 30 WEST        TOLEDO   52342   \n",
            "8  522 MULBERRY, SUITE A     MUSCATINE   52761   \n",
            "9           117 IOWA AVE        DUNLAP   712-2   \n",
            "\n",
            "                                       storeLocation  county_number  \\\n",
            "0    1013 MAIN\\nKEOKUK 52632\\n(40.39978, -91.387531)             56   \n",
            "1  900 E WASHINGTON\\nCLARINDA 51632\\n(40.739238, ...             73   \n",
            "2  1414 48TH ST\\nFORT MADISON 52627\\n(40.624226, ...             56   \n",
            "3                   812 S 1ST AVE\\nIOWA CITY 52240\\n             52   \n",
            "4  104 HIGHWAY 30 WEST\\nTOLEDO 52342\\n(41.985887,...             86   \n",
            "5  118 South Main St.\\nHOLSTEIN 51025\\n(42.490073...             47   \n",
            "6  1422 FLAMMANG DR\\nWATERLOO 50702\\n(42.459938, ...              7   \n",
            "7  104 HIGHWAY 30 WEST\\nTOLEDO 52342\\n(41.985887,...             86   \n",
            "8           522 MULBERRY, SUITE A\\nMUSCATINE 52761\\n             70   \n",
            "9  117 IOWA AVE\\nDUNLAP 712-2\\n(41.854728, -95.60...             43   \n",
            "\n",
            "       county  ...  itemno                                        im_desc  \\\n",
            "0         Lee  ...     297                          Templeton Rye w/Flask   \n",
            "1        Page  ...     297                          Templeton Rye w/Flask   \n",
            "2         Lee  ...     249  Disaronno Amaretto Cavalli Mignon 3-50ml Pack   \n",
            "3     Johnson  ...     237                 Knob Creek w/ Crystal Decanter   \n",
            "4        Tama  ...     249  Disaronno Amaretto Cavalli Mignon 3-50ml Pack   \n",
            "5         Ida  ...     237                 Knob Creek w/ Crystal Decanter   \n",
            "6  Black Hawk  ...     238                   Forbidden Secret Coffee Pack   \n",
            "7        Tama  ...     237                 Knob Creek w/ Crystal Decanter   \n",
            "8   Muscatine  ...     173                    Laphroaig w/ Whiskey Stones   \n",
            "9    Harrison  ...     249  Disaronno Amaretto Cavalli Mignon 3-50ml Pack   \n",
            "\n",
            "   pack bottle_volume_ml  state_bottle_cost state_bottle_retail  sale_bottles  \\\n",
            "0     6              750             $18.09              $27.14             6   \n",
            "1     6              750             $18.09              $27.14            12   \n",
            "2    20              150              $6.40               $9.60             2   \n",
            "3     3             1750             $35.55              $53.34             3   \n",
            "4    20              150              $6.40               $9.60             2   \n",
            "5     3             1750             $35.55              $53.34             1   \n",
            "6     6             1500             $11.62              $17.43             6   \n",
            "7     3             1750             $35.55              $53.34             2   \n",
            "8    12              750             $19.58              $29.37             4   \n",
            "9    20              150              $6.40               $9.60             2   \n",
            "\n",
            "   sale_dollars sale_liters sale_gallons  \n",
            "0       $162.84        4.50         1.19  \n",
            "1       $325.68        9.00         2.38  \n",
            "2        $19.20        0.30         0.08  \n",
            "3       $160.02        5.25         1.39  \n",
            "4        $19.20        0.30         0.08  \n",
            "5        $53.34        1.75         0.46  \n",
            "6       $104.58        9.00         2.38  \n",
            "7       $106.68        3.50         0.92  \n",
            "8       $117.48        3.00         0.79  \n",
            "9        $19.20        0.30         0.08  \n",
            "\n",
            "[10 rows x 24 columns]\n"
          ]
        },
        {
          "output_type": "execute_result",
          "data": {
            "text/plain": [
              "  invoice_line_no       date  store                               name  \\\n",
              "0    S29198800001 2015-11-20   2191                     Keokuk Spirits   \n",
              "1    S29195400002 2015-11-21   2205             Ding's Honk And Holler   \n",
              "2    S29050300001 2015-11-16   3549               Quicker Liquor Store   \n",
              "3    S28867700001 2015-11-04   2513   Hy-Vee Food Store #2 / Iowa City   \n",
              "4    S29050800001 2015-11-17   3942                   Twin Town Liquor   \n",
              "5    S28869200001 2015-11-11   3650         Spirits, Stogies and Stuff   \n",
              "6    S28865700001 2015-11-09   2538    Hy-Vee Food Store #3 / Waterloo   \n",
              "7    S28869500001 2015-11-10   3942                   Twin Town Liquor   \n",
              "8    S29339300091 2015-11-30   2662  Hy-Vee Wine & Spirits / Muscatine   \n",
              "9    S29050900001 2015-11-16   4307         Crossroads Wine and Liquor   \n",
              "\n",
              "                 address          city zipcode  \\\n",
              "0              1013 MAIN        KEOKUK   52632   \n",
              "1       900 E WASHINGTON      CLARINDA   51632   \n",
              "2           1414 48TH ST  FORT MADISON   52627   \n",
              "3         812  S 1ST AVE     IOWA CITY   52240   \n",
              "4    104 HIGHWAY 30 WEST        TOLEDO   52342   \n",
              "5     118 South Main St.      HOLSTEIN   51025   \n",
              "6       1422 FLAMMANG DR      WATERLOO   50702   \n",
              "7    104 HIGHWAY 30 WEST        TOLEDO   52342   \n",
              "8  522 MULBERRY, SUITE A     MUSCATINE   52761   \n",
              "9           117 IOWA AVE        DUNLAP   712-2   \n",
              "\n",
              "                                       storeLocation  county_number  \\\n",
              "0    1013 MAIN\\nKEOKUK 52632\\n(40.39978, -91.387531)             56   \n",
              "1  900 E WASHINGTON\\nCLARINDA 51632\\n(40.739238, ...             73   \n",
              "2  1414 48TH ST\\nFORT MADISON 52627\\n(40.624226, ...             56   \n",
              "3                   812 S 1ST AVE\\nIOWA CITY 52240\\n             52   \n",
              "4  104 HIGHWAY 30 WEST\\nTOLEDO 52342\\n(41.985887,...             86   \n",
              "5  118 South Main St.\\nHOLSTEIN 51025\\n(42.490073...             47   \n",
              "6  1422 FLAMMANG DR\\nWATERLOO 50702\\n(42.459938, ...              7   \n",
              "7  104 HIGHWAY 30 WEST\\nTOLEDO 52342\\n(41.985887,...             86   \n",
              "8           522 MULBERRY, SUITE A\\nMUSCATINE 52761\\n             70   \n",
              "9  117 IOWA AVE\\nDUNLAP 712-2\\n(41.854728, -95.60...             43   \n",
              "\n",
              "       county  ...  itemno                                        im_desc  \\\n",
              "0         Lee  ...     297                          Templeton Rye w/Flask   \n",
              "1        Page  ...     297                          Templeton Rye w/Flask   \n",
              "2         Lee  ...     249  Disaronno Amaretto Cavalli Mignon 3-50ml Pack   \n",
              "3     Johnson  ...     237                 Knob Creek w/ Crystal Decanter   \n",
              "4        Tama  ...     249  Disaronno Amaretto Cavalli Mignon 3-50ml Pack   \n",
              "5         Ida  ...     237                 Knob Creek w/ Crystal Decanter   \n",
              "6  Black Hawk  ...     238                   Forbidden Secret Coffee Pack   \n",
              "7        Tama  ...     237                 Knob Creek w/ Crystal Decanter   \n",
              "8   Muscatine  ...     173                    Laphroaig w/ Whiskey Stones   \n",
              "9    Harrison  ...     249  Disaronno Amaretto Cavalli Mignon 3-50ml Pack   \n",
              "\n",
              "   pack bottle_volume_ml  state_bottle_cost state_bottle_retail  sale_bottles  \\\n",
              "0     6              750             $18.09              $27.14             6   \n",
              "1     6              750             $18.09              $27.14            12   \n",
              "2    20              150              $6.40               $9.60             2   \n",
              "3     3             1750             $35.55              $53.34             3   \n",
              "4    20              150              $6.40               $9.60             2   \n",
              "5     3             1750             $35.55              $53.34             1   \n",
              "6     6             1500             $11.62              $17.43             6   \n",
              "7     3             1750             $35.55              $53.34             2   \n",
              "8    12              750             $19.58              $29.37             4   \n",
              "9    20              150              $6.40               $9.60             2   \n",
              "\n",
              "   sale_dollars sale_liters sale_gallons  \n",
              "0       $162.84        4.50         1.19  \n",
              "1       $325.68        9.00         2.38  \n",
              "2        $19.20        0.30         0.08  \n",
              "3       $160.02        5.25         1.39  \n",
              "4        $19.20        0.30         0.08  \n",
              "5        $53.34        1.75         0.46  \n",
              "6       $104.58        9.00         2.38  \n",
              "7       $106.68        3.50         0.92  \n",
              "8       $117.48        3.00         0.79  \n",
              "9        $19.20        0.30         0.08  \n",
              "\n",
              "[10 rows x 24 columns]"
            ],
            "text/html": [
              "\n",
              "  <div id=\"df-054dae58-912e-43d7-a44a-bfe7c352ac57\">\n",
              "    <div class=\"colab-df-container\">\n",
              "      <div>\n",
              "<style scoped>\n",
              "    .dataframe tbody tr th:only-of-type {\n",
              "        vertical-align: middle;\n",
              "    }\n",
              "\n",
              "    .dataframe tbody tr th {\n",
              "        vertical-align: top;\n",
              "    }\n",
              "\n",
              "    .dataframe thead th {\n",
              "        text-align: right;\n",
              "    }\n",
              "</style>\n",
              "<table border=\"1\" class=\"dataframe\">\n",
              "  <thead>\n",
              "    <tr style=\"text-align: right;\">\n",
              "      <th></th>\n",
              "      <th>invoice_line_no</th>\n",
              "      <th>date</th>\n",
              "      <th>store</th>\n",
              "      <th>name</th>\n",
              "      <th>address</th>\n",
              "      <th>city</th>\n",
              "      <th>zipcode</th>\n",
              "      <th>storeLocation</th>\n",
              "      <th>county_number</th>\n",
              "      <th>county</th>\n",
              "      <th>...</th>\n",
              "      <th>itemno</th>\n",
              "      <th>im_desc</th>\n",
              "      <th>pack</th>\n",
              "      <th>bottle_volume_ml</th>\n",
              "      <th>state_bottle_cost</th>\n",
              "      <th>state_bottle_retail</th>\n",
              "      <th>sale_bottles</th>\n",
              "      <th>sale_dollars</th>\n",
              "      <th>sale_liters</th>\n",
              "      <th>sale_gallons</th>\n",
              "    </tr>\n",
              "  </thead>\n",
              "  <tbody>\n",
              "    <tr>\n",
              "      <th>0</th>\n",
              "      <td>S29198800001</td>\n",
              "      <td>2015-11-20</td>\n",
              "      <td>2191</td>\n",
              "      <td>Keokuk Spirits</td>\n",
              "      <td>1013 MAIN</td>\n",
              "      <td>KEOKUK</td>\n",
              "      <td>52632</td>\n",
              "      <td>1013 MAIN\\nKEOKUK 52632\\n(40.39978, -91.387531)</td>\n",
              "      <td>56</td>\n",
              "      <td>Lee</td>\n",
              "      <td>...</td>\n",
              "      <td>297</td>\n",
              "      <td>Templeton Rye w/Flask</td>\n",
              "      <td>6</td>\n",
              "      <td>750</td>\n",
              "      <td>$18.09</td>\n",
              "      <td>$27.14</td>\n",
              "      <td>6</td>\n",
              "      <td>$162.84</td>\n",
              "      <td>4.50</td>\n",
              "      <td>1.19</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>1</th>\n",
              "      <td>S29195400002</td>\n",
              "      <td>2015-11-21</td>\n",
              "      <td>2205</td>\n",
              "      <td>Ding's Honk And Holler</td>\n",
              "      <td>900 E WASHINGTON</td>\n",
              "      <td>CLARINDA</td>\n",
              "      <td>51632</td>\n",
              "      <td>900 E WASHINGTON\\nCLARINDA 51632\\n(40.739238, ...</td>\n",
              "      <td>73</td>\n",
              "      <td>Page</td>\n",
              "      <td>...</td>\n",
              "      <td>297</td>\n",
              "      <td>Templeton Rye w/Flask</td>\n",
              "      <td>6</td>\n",
              "      <td>750</td>\n",
              "      <td>$18.09</td>\n",
              "      <td>$27.14</td>\n",
              "      <td>12</td>\n",
              "      <td>$325.68</td>\n",
              "      <td>9.00</td>\n",
              "      <td>2.38</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>2</th>\n",
              "      <td>S29050300001</td>\n",
              "      <td>2015-11-16</td>\n",
              "      <td>3549</td>\n",
              "      <td>Quicker Liquor Store</td>\n",
              "      <td>1414 48TH ST</td>\n",
              "      <td>FORT MADISON</td>\n",
              "      <td>52627</td>\n",
              "      <td>1414 48TH ST\\nFORT MADISON 52627\\n(40.624226, ...</td>\n",
              "      <td>56</td>\n",
              "      <td>Lee</td>\n",
              "      <td>...</td>\n",
              "      <td>249</td>\n",
              "      <td>Disaronno Amaretto Cavalli Mignon 3-50ml Pack</td>\n",
              "      <td>20</td>\n",
              "      <td>150</td>\n",
              "      <td>$6.40</td>\n",
              "      <td>$9.60</td>\n",
              "      <td>2</td>\n",
              "      <td>$19.20</td>\n",
              "      <td>0.30</td>\n",
              "      <td>0.08</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>3</th>\n",
              "      <td>S28867700001</td>\n",
              "      <td>2015-11-04</td>\n",
              "      <td>2513</td>\n",
              "      <td>Hy-Vee Food Store #2 / Iowa City</td>\n",
              "      <td>812  S 1ST AVE</td>\n",
              "      <td>IOWA CITY</td>\n",
              "      <td>52240</td>\n",
              "      <td>812 S 1ST AVE\\nIOWA CITY 52240\\n</td>\n",
              "      <td>52</td>\n",
              "      <td>Johnson</td>\n",
              "      <td>...</td>\n",
              "      <td>237</td>\n",
              "      <td>Knob Creek w/ Crystal Decanter</td>\n",
              "      <td>3</td>\n",
              "      <td>1750</td>\n",
              "      <td>$35.55</td>\n",
              "      <td>$53.34</td>\n",
              "      <td>3</td>\n",
              "      <td>$160.02</td>\n",
              "      <td>5.25</td>\n",
              "      <td>1.39</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>4</th>\n",
              "      <td>S29050800001</td>\n",
              "      <td>2015-11-17</td>\n",
              "      <td>3942</td>\n",
              "      <td>Twin Town Liquor</td>\n",
              "      <td>104 HIGHWAY 30 WEST</td>\n",
              "      <td>TOLEDO</td>\n",
              "      <td>52342</td>\n",
              "      <td>104 HIGHWAY 30 WEST\\nTOLEDO 52342\\n(41.985887,...</td>\n",
              "      <td>86</td>\n",
              "      <td>Tama</td>\n",
              "      <td>...</td>\n",
              "      <td>249</td>\n",
              "      <td>Disaronno Amaretto Cavalli Mignon 3-50ml Pack</td>\n",
              "      <td>20</td>\n",
              "      <td>150</td>\n",
              "      <td>$6.40</td>\n",
              "      <td>$9.60</td>\n",
              "      <td>2</td>\n",
              "      <td>$19.20</td>\n",
              "      <td>0.30</td>\n",
              "      <td>0.08</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>5</th>\n",
              "      <td>S28869200001</td>\n",
              "      <td>2015-11-11</td>\n",
              "      <td>3650</td>\n",
              "      <td>Spirits, Stogies and Stuff</td>\n",
              "      <td>118 South Main St.</td>\n",
              "      <td>HOLSTEIN</td>\n",
              "      <td>51025</td>\n",
              "      <td>118 South Main St.\\nHOLSTEIN 51025\\n(42.490073...</td>\n",
              "      <td>47</td>\n",
              "      <td>Ida</td>\n",
              "      <td>...</td>\n",
              "      <td>237</td>\n",
              "      <td>Knob Creek w/ Crystal Decanter</td>\n",
              "      <td>3</td>\n",
              "      <td>1750</td>\n",
              "      <td>$35.55</td>\n",
              "      <td>$53.34</td>\n",
              "      <td>1</td>\n",
              "      <td>$53.34</td>\n",
              "      <td>1.75</td>\n",
              "      <td>0.46</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>6</th>\n",
              "      <td>S28865700001</td>\n",
              "      <td>2015-11-09</td>\n",
              "      <td>2538</td>\n",
              "      <td>Hy-Vee Food Store #3 / Waterloo</td>\n",
              "      <td>1422 FLAMMANG DR</td>\n",
              "      <td>WATERLOO</td>\n",
              "      <td>50702</td>\n",
              "      <td>1422 FLAMMANG DR\\nWATERLOO 50702\\n(42.459938, ...</td>\n",
              "      <td>7</td>\n",
              "      <td>Black Hawk</td>\n",
              "      <td>...</td>\n",
              "      <td>238</td>\n",
              "      <td>Forbidden Secret Coffee Pack</td>\n",
              "      <td>6</td>\n",
              "      <td>1500</td>\n",
              "      <td>$11.62</td>\n",
              "      <td>$17.43</td>\n",
              "      <td>6</td>\n",
              "      <td>$104.58</td>\n",
              "      <td>9.00</td>\n",
              "      <td>2.38</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>7</th>\n",
              "      <td>S28869500001</td>\n",
              "      <td>2015-11-10</td>\n",
              "      <td>3942</td>\n",
              "      <td>Twin Town Liquor</td>\n",
              "      <td>104 HIGHWAY 30 WEST</td>\n",
              "      <td>TOLEDO</td>\n",
              "      <td>52342</td>\n",
              "      <td>104 HIGHWAY 30 WEST\\nTOLEDO 52342\\n(41.985887,...</td>\n",
              "      <td>86</td>\n",
              "      <td>Tama</td>\n",
              "      <td>...</td>\n",
              "      <td>237</td>\n",
              "      <td>Knob Creek w/ Crystal Decanter</td>\n",
              "      <td>3</td>\n",
              "      <td>1750</td>\n",
              "      <td>$35.55</td>\n",
              "      <td>$53.34</td>\n",
              "      <td>2</td>\n",
              "      <td>$106.68</td>\n",
              "      <td>3.50</td>\n",
              "      <td>0.92</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>8</th>\n",
              "      <td>S29339300091</td>\n",
              "      <td>2015-11-30</td>\n",
              "      <td>2662</td>\n",
              "      <td>Hy-Vee Wine &amp; Spirits / Muscatine</td>\n",
              "      <td>522 MULBERRY, SUITE A</td>\n",
              "      <td>MUSCATINE</td>\n",
              "      <td>52761</td>\n",
              "      <td>522 MULBERRY, SUITE A\\nMUSCATINE 52761\\n</td>\n",
              "      <td>70</td>\n",
              "      <td>Muscatine</td>\n",
              "      <td>...</td>\n",
              "      <td>173</td>\n",
              "      <td>Laphroaig w/ Whiskey Stones</td>\n",
              "      <td>12</td>\n",
              "      <td>750</td>\n",
              "      <td>$19.58</td>\n",
              "      <td>$29.37</td>\n",
              "      <td>4</td>\n",
              "      <td>$117.48</td>\n",
              "      <td>3.00</td>\n",
              "      <td>0.79</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>9</th>\n",
              "      <td>S29050900001</td>\n",
              "      <td>2015-11-16</td>\n",
              "      <td>4307</td>\n",
              "      <td>Crossroads Wine and Liquor</td>\n",
              "      <td>117 IOWA AVE</td>\n",
              "      <td>DUNLAP</td>\n",
              "      <td>712-2</td>\n",
              "      <td>117 IOWA AVE\\nDUNLAP 712-2\\n(41.854728, -95.60...</td>\n",
              "      <td>43</td>\n",
              "      <td>Harrison</td>\n",
              "      <td>...</td>\n",
              "      <td>249</td>\n",
              "      <td>Disaronno Amaretto Cavalli Mignon 3-50ml Pack</td>\n",
              "      <td>20</td>\n",
              "      <td>150</td>\n",
              "      <td>$6.40</td>\n",
              "      <td>$9.60</td>\n",
              "      <td>2</td>\n",
              "      <td>$19.20</td>\n",
              "      <td>0.30</td>\n",
              "      <td>0.08</td>\n",
              "    </tr>\n",
              "  </tbody>\n",
              "</table>\n",
              "<p>10 rows × 24 columns</p>\n",
              "</div>\n",
              "      <button class=\"colab-df-convert\" onclick=\"convertToInteractive('df-054dae58-912e-43d7-a44a-bfe7c352ac57')\"\n",
              "              title=\"Convert this dataframe to an interactive table.\"\n",
              "              style=\"display:none;\">\n",
              "        \n",
              "  <svg xmlns=\"http://www.w3.org/2000/svg\" height=\"24px\"viewBox=\"0 0 24 24\"\n",
              "       width=\"24px\">\n",
              "    <path d=\"M0 0h24v24H0V0z\" fill=\"none\"/>\n",
              "    <path d=\"M18.56 5.44l.94 2.06.94-2.06 2.06-.94-2.06-.94-.94-2.06-.94 2.06-2.06.94zm-11 1L8.5 8.5l.94-2.06 2.06-.94-2.06-.94L8.5 2.5l-.94 2.06-2.06.94zm10 10l.94 2.06.94-2.06 2.06-.94-2.06-.94-.94-2.06-.94 2.06-2.06.94z\"/><path d=\"M17.41 7.96l-1.37-1.37c-.4-.4-.92-.59-1.43-.59-.52 0-1.04.2-1.43.59L10.3 9.45l-7.72 7.72c-.78.78-.78 2.05 0 2.83L4 21.41c.39.39.9.59 1.41.59.51 0 1.02-.2 1.41-.59l7.78-7.78 2.81-2.81c.8-.78.8-2.07 0-2.86zM5.41 20L4 18.59l7.72-7.72 1.47 1.35L5.41 20z\"/>\n",
              "  </svg>\n",
              "      </button>\n",
              "      \n",
              "  <style>\n",
              "    .colab-df-container {\n",
              "      display:flex;\n",
              "      flex-wrap:wrap;\n",
              "      gap: 12px;\n",
              "    }\n",
              "\n",
              "    .colab-df-convert {\n",
              "      background-color: #E8F0FE;\n",
              "      border: none;\n",
              "      border-radius: 50%;\n",
              "      cursor: pointer;\n",
              "      display: none;\n",
              "      fill: #1967D2;\n",
              "      height: 32px;\n",
              "      padding: 0 0 0 0;\n",
              "      width: 32px;\n",
              "    }\n",
              "\n",
              "    .colab-df-convert:hover {\n",
              "      background-color: #E2EBFA;\n",
              "      box-shadow: 0px 1px 2px rgba(60, 64, 67, 0.3), 0px 1px 3px 1px rgba(60, 64, 67, 0.15);\n",
              "      fill: #174EA6;\n",
              "    }\n",
              "\n",
              "    [theme=dark] .colab-df-convert {\n",
              "      background-color: #3B4455;\n",
              "      fill: #D2E3FC;\n",
              "    }\n",
              "\n",
              "    [theme=dark] .colab-df-convert:hover {\n",
              "      background-color: #434B5C;\n",
              "      box-shadow: 0px 1px 3px 1px rgba(0, 0, 0, 0.15);\n",
              "      filter: drop-shadow(0px 1px 2px rgba(0, 0, 0, 0.3));\n",
              "      fill: #FFFFFF;\n",
              "    }\n",
              "  </style>\n",
              "\n",
              "      <script>\n",
              "        const buttonEl =\n",
              "          document.querySelector('#df-054dae58-912e-43d7-a44a-bfe7c352ac57 button.colab-df-convert');\n",
              "        buttonEl.style.display =\n",
              "          google.colab.kernel.accessAllowed ? 'block' : 'none';\n",
              "\n",
              "        async function convertToInteractive(key) {\n",
              "          const element = document.querySelector('#df-054dae58-912e-43d7-a44a-bfe7c352ac57');\n",
              "          const dataTable =\n",
              "            await google.colab.kernel.invokeFunction('convertToInteractive',\n",
              "                                                     [key], {});\n",
              "          if (!dataTable) return;\n",
              "\n",
              "          const docLinkHtml = 'Like what you see? Visit the ' +\n",
              "            '<a target=\"_blank\" href=https://colab.research.google.com/notebooks/data_table.ipynb>data table notebook</a>'\n",
              "            + ' to learn more about interactive tables.';\n",
              "          element.innerHTML = '';\n",
              "          dataTable['output_type'] = 'display_data';\n",
              "          await google.colab.output.renderOutput(dataTable, element);\n",
              "          const docLink = document.createElement('div');\n",
              "          docLink.innerHTML = docLinkHtml;\n",
              "          element.appendChild(docLink);\n",
              "        }\n",
              "      </script>\n",
              "    </div>\n",
              "  </div>\n",
              "  "
            ]
          },
          "metadata": {},
          "execution_count": 6
        }
      ],
      "source": [
        "runq(\"select * from iowa limit 10\")"
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "pXQEjpzT_z8o"
      },
      "source": [
        "__Disclaimer: this course does not condone drinking, we are using this dataset because it is a common format for a sales transaction log in a silghtly more accessible domain than typical bank transactions__."
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "bhOY3xiZ_z8o"
      },
      "source": [
        "## Part I: SQL, the sequel"
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "IVHMm1wp_z8o"
      },
      "source": [
        "### Jupyter Notes: _Read these carefully_\n",
        "\n",
        "* You **may** create new IPython notebook cells to use for e.g. testing, debugging, exploring, etc.- this is encouraged in fact!- **just make sure that you run the final cell to submit your results**\n",
        "  * you can press shift+enter to execute to code in the cell that your cursor is in.\n",
        "* When you see `In [*]:` to the left of the cell you are executing, this means that the code / query is _running_. Please wait for the execution to complete\n",
        "    * **If the cell is hanging- i.e. running for too long: you can restart the kernel**\n",
        "    * To restart kernel using the menu bar: \"Kernel >> Restart >> Clear all outputs & restart\"), then re-execute cells from the top\n",
        "* _Have fun!_"
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "F5_O3o-g_z8p"
      },
      "source": [
        "__Now, please write the SQL query for each of the following questions.__\n",
        "\n",
        "__Fill answers according to instruction in each question. Make sure to submit your query also (instruction given).__\n",
        "\n",
        "Note: Some queries will take a few minutes to run on your virtual machine. If your query is running for more than ~10 minutes, you either did something wrong, \n",
        "or you may need to create tables with your temp tables to run the query more efficiently. \n",
        "\n",
        "For example: If you use the results of a sub-query multiple times, it \n",
        "can help to use SELECT ... INTO ... then reference that table.\n"
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "_KJajl9o_z8p"
      },
      "source": [
        "### __(2 points) Q1.1: Which store had the most sales in terms of total records in the table?__"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "id": "8amyd-Eq_z8q"
      },
      "outputs": [],
      "source": [
        "q11 = \"\"\"\n",
        "YOUR QUERY HERE.  CAN BE MULTILINE\n",
        "\"\"\"\n",
        "\n",
        "runq(q11)"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "id": "AiFu6MyD_z8q"
      },
      "outputs": [],
      "source": [
        "# Please replace None with the result store id and record count here\n",
        "# submit query in string format\n",
        "results['q1'] = {\n",
        "    'store': None,\n",
        "    'count': None,\n",
        "    'query': q11\n",
        "}"
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "5V0S1kwL_z8q"
      },
      "source": [
        "### __(2 points) Q1.2: At the store with the most total records (answer to Q1.1), what was the vendor_no with most sale records? (The vendor that has the most number of records for that store?)__"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 1,
      "metadata": {
        "id": "-FtQX3AZ_z8r",
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 204
        },
        "outputId": "65edd8a9-e248-4198-8a75-a0c9661a7e28"
      },
      "outputs": [
        {
          "output_type": "error",
          "ename": "NameError",
          "evalue": "ignored",
          "traceback": [
            "\u001b[0;31m---------------------------------------------------------------------------\u001b[0m",
            "\u001b[0;31mNameError\u001b[0m                                 Traceback (most recent call last)",
            "\u001b[0;32m<ipython-input-1-e47b1f3f72a7>\u001b[0m in \u001b[0;36m<module>\u001b[0;34m\u001b[0m\n\u001b[1;32m      2\u001b[0m \u001b[0mYOUR\u001b[0m \u001b[0mQUERY\u001b[0m \u001b[0mHERE\u001b[0m\u001b[0;34m.\u001b[0m   \u001b[0mCAN\u001b[0m \u001b[0mBE\u001b[0m \u001b[0mMULTILINE\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m      3\u001b[0m \"\"\"\n\u001b[0;32m----> 4\u001b[0;31m \u001b[0mrunq\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0mq12\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0m",
            "\u001b[0;31mNameError\u001b[0m: name 'runq' is not defined"
          ]
        }
      ],
      "source": [
        "q12 = \"\"\"\n",
        "YOUR QUERY HERE.  CAN BE MULTILINE\n",
        "\"\"\"\n",
        "runq(q12)\n"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "id": "OLmnoung_z8r"
      },
      "outputs": [],
      "source": [
        "# please replace None with the result vendor_no and count here\n",
        "# submit query in string format\n",
        "results['q2'] = {\n",
        "    'vendor_no': None,\n",
        "    'count': None,\n",
        "    'query': q12\n",
        "}"
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "t_YkKA_Z_z8r"
      },
      "source": [
        "### (3 points) Q1.3: For each zipcode, compute the single most purchased category_name by total sale_bottles. \n",
        "\n",
        "__Return the top 5 (zipcode, category_name) when sorted in descending order by qty, where qty is the most purchased total sale_bottles.__"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "id": "d96YZ9iU_z8s"
      },
      "outputs": [],
      "source": [
        "q13 = \"\"\"\n",
        "YOUR QUERY HERE.  CAN BE MULTILINE\n",
        "\"\"\"\n",
        "\n",
        "runq(q13)"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "id": "W78wW7lc_z8s"
      },
      "outputs": [],
      "source": [
        "# please replace None in the following\n",
        "# submit query in string format\n",
        "results['q3'] = {\n",
        "    1: {'zipcode': None, 'category_name': None, 'qty': None},\n",
        "    2: {'zipcode': None, 'category_name': None, 'qty': None},\n",
        "    3: {'zipcode': None, 'category_name': None, 'qty': None},\n",
        "    4: {'zipcode': None, 'category_name': None, 'qty': None},\n",
        "    5: {'zipcode': None, 'category_name': None, 'qty': None},\n",
        "    'query': q13\n",
        "}"
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "P37uxzU__z8s"
      },
      "source": [
        "### (3 points) Q1.4: This problem has two steps, you only need to return the value from the second step.\n",
        "\n",
        "__Compute the set of all liquors with the characters \"Lagavulin\" (case sensitive) in its description (`im_desc`). The attribute `itemno` can serve as a unique identifier for a specific liquor type.__\n",
        "\n",
        "__Return the number of distinct `zipcodes` for all liquor stores that sold at least two of every Lagavulin liquor type, as defined in the previous sentence.__\n",
        "\n",
        "(Optional: It is possible to rewrite the query in a form that can execute quite fast, but it will require you to create some temporary tables (for instance, via the WITH clause) and/or experiment with alternate forms to express the problem. If you find the solution, feel free to submit it!)"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "id": "OJocgeg8_z8s"
      },
      "outputs": [],
      "source": [
        "q14 = \"\"\"\n",
        "YOUR QUERY HERE.  CAN BE MULTILINE\n",
        "\"\"\"\n",
        "\n",
        "runq(q14)"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "id": "v9GtsnfS_z8s"
      },
      "outputs": [],
      "source": [
        "# please replace None with the according count here\n",
        "# submit query in string format\n",
        "results['q4'] = {\n",
        "    'count': None,\n",
        "    'query': q14\n",
        "}"
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "zQC_d57d_z8t"
      },
      "source": [
        "### (3 points) Q1.5:  What is the item number (`itemno`) of the liquor and name (`name`) of the store where the difference between the liquor's $cost\\_per\\_ml$ at a store and its $cost\\_per\\_ml$ state-wide is largest (as defined below)?\n",
        "\n",
        "Let a liquor's $cost\\_per\\_ml$ $ = \\frac{state\\_bottle\\_retail}{bottle\\_volume\\_ml}$ while the state-wide $cost\\_per\\_ml$ is equal to the average of a liquor's $cost\\_per\\_ml$ across all stores."
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "id": "K2Vv4ZT__z8t"
      },
      "outputs": [],
      "source": [
        "q15 = \"\"\"\n",
        "YOUR QUERY HERE.  CAN BE MULTILINE\n",
        "\"\"\"\n",
        "\n",
        "runq(q15)"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "id": "1xZExeiS_z8t"
      },
      "outputs": [],
      "source": [
        "# please replace None with the item number here\n",
        "# submit query in string format\n",
        "results['q5'] = {\n",
        "    'itemno': None,\n",
        "    'query': q15\n",
        "}"
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "ig6F9MMv_z8t"
      },
      "source": [
        "### (3 points) Q1.6: Write a short paragraph about the main differences between writing Python code and writing SQL. List one pro and one con for each approach. "
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "id": "m8LI-Ybz_z8t"
      },
      "outputs": [],
      "source": [
        "results['q6'] = {\n",
        "    # put Python's pros and cons here\n",
        "    # please write in the quotes\n",
        "    'python_pros': \"\"\" PROS HERE \"\"\",\n",
        "    'python_cons': \"\"\" CONS HERE\"\"\",\n",
        "    'sql_pros': \"\"\"PROS HERE\"\"\",\n",
        "    'sql_cons': \"\"\"CONS HERE\"\"\"\n",
        "}"
      ]
    },
    {
      "cell_type": "markdown",
      "source": [
        "# Submit Your Results\n",
        "\n",
        "Clean up your codes and double check that:\n",
        "\n",
        "1.   Your result is reproducible. You may want to restart runtime (Ctrl M .) and run all the codes again (Ctrl F9).\n",
        "2.   You don't use any modules beyond [Python Standard Library](https://docs.python.org/3/library/).\n",
        "3.   You don't run any operating system shell command (prepended by exclamation point) besides the setup codes we provided.\n",
        "4. Your `results` variable's format is not different from what was given in the base code.\n",
        "\n",
        "After that, save your notebook as a python file:\n",
        "\n",
        "1.   Click on the \"file\" on the top toolbar.\n",
        "2.   Click on the \"Download\" then \"Download .py\" (Note that not \"Download .ipynb\").\n",
        "3.   Name the file \"hw3.py\" and download the file to your local storage.\n",
        "![image.png](data:image/png;base64,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)\n",
        "\n",
        "Upload the \"hw3.py\" to Gradescope \"HW3 Programming.\" We have tests to check that your .py file is executable. Make sure you pass the first two tests."
      ],
      "metadata": {
        "id": "dIeARBb5vMK_"
      }
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "mhDXB5qu_z8u"
      },
      "source": [
        "## Part II, Normalization\n",
        "\n",
        "See Github page for more details. Submit __hard copy__ for Part 2 as instructed __before due__."
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "ZFCh9Vae_z8u"
      },
      "source": [
        "_Remarks: Dataset sourced from https://data.iowa.gov/Economy/Iowa-Liquor-Sales/m3tr-qhgy. 1mil tuples extracted and preprocessed to remove double quotation marks and apostrophes._"
      ]
    }
  ],
  "metadata": {
    "colab": {
      "collapsed_sections": [],
      "provenance": []
    },
    "kernelspec": {
      "display_name": "Python 3",
      "language": "python",
      "name": "python3"
    },
    "language_info": {
      "codemirror_mode": {
        "name": "ipython",
        "version": 3
      },
      "file_extension": ".py",
      "mimetype": "text/x-python",
      "name": "python",
      "nbconvert_exporter": "python",
      "pygments_lexer": "ipython3",
      "version": "3.8.2"
    }
  },
  "nbformat": 4,
  "nbformat_minor": 0
}