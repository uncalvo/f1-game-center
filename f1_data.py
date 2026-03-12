import random
import unicodedata
from collections import defaultdict

# ══════════════════════════════════════════════════════════════════
#  BASE DE DATOS — FÓRMULA 1
#  (equipos, nacionalidad, victorias, podios, campeón_mundial)
# ══════════════════════════════════════════════════════════════════
RAW_F1 = {
    "fernando alonso"       : (["minardi","renault","mclaren","ferrari","alpine","aston martin"],           "española",        32, 106, 2, 2001, "", 1981, 22, 0),
    "lewis hamilton"        : (["mclaren","mercedes","ferrari"],                                            "británica",      104, 197, 7, 2007, "mclaren", 1985, 19, 0),
    "valtteri bottas"       : (["williams","mercedes","alfa romeo","sauber","cadillac"],                    "finlandesa",      10,  67, False, 2013, "", 1989, 12, 2024),
    "kimi raikkonen"        : (["sauber","mclaren","ferrari","lotus","alfa romeo"],                         "finlandesa",      21, 103, 1, 2001, "", 1979, 19, 2021),
    "sebastian vettel"      : (["bmw sauber","toro rosso","red bull","ferrari","aston martin"],             "alemana",         91, 122, 4, 2007, "red bull", 1987, 16, 2022),
    "daniel ricciardo"      : (["hrt","toro rosso","red bull","renault","mclaren","alphatauri","racing bulls"], "australiana", 8,  32, False, 2011, "red bull", 1989, 1, 2024),
    "sergio perez"          : (["sauber","mclaren","force india","racing point","red bull","cadillac"],     "mexicana",         7,  40, False, 2011, "", 1990, 14, 2024),
    "carlos sainz"          : (["toro rosso","renault","mclaren","ferrari","williams"],                     "española",         3,  23, False, 2015, "red bull", 1994, 11, 0),
    "charles leclerc"       : (["sauber","ferrari"],                                                        "monegasca",        7,  42, False, 2018, "ferrari", 1997, 8, 0),
    "george russell"        : (["williams","mercedes"],                                                     "británica",        3,  21, False, 2019, "mercedes", 1998, 6, 0),
    "nico hulkenberg"       : (["williams","force india","sauber","renault","racing point","aston martin","haas","audi"], "alemana", 0, 0, False, 2010, "", 1987, 11, 0),
    "esteban ocon"          : (["manor","force india","racing point","renault","alpine","haas"],             "francesa",         1,   3, False, 2016, "mercedes", 1996, 7, 0),
    "pierre gasly"          : (["toro rosso","red bull","alphatauri","alpine"],                              "francesa",         1,   4, False, 2017, "red bull", 1996, 8, 0),
    "alex albon"            : (["toro rosso","red bull","williams"],                                         "tailandesa",       0,   2, False, 2019, "red bull", 1996, 5, 0),
    "lando norris"          : (["mclaren"],                                                                  "británica",        4,  34, False, 2019, "mclaren", 1999, 7, 0),
    "max verstappen"        : (["toro rosso","red bull"],                                                    "neerlandesa",     63,  98, 4, 2015, "red bull", 1997, 11, 0),
    "oliver bearman"        : (["ferrari","haas"],                                                           "británica",        0,   0, False, 2023, "ferrari", 2005, 1, 0),
    "gabriel bortoleto"     : (["sauber","audi"],                                                            "brasileña",        0,   0, False, 2025, "", 2004, 1, 0),
    "liam lawson"           : (["alphatauri","red bull","racing bulls"],                                      "neozelandesa",     0,   0, False, 2023, "red bull", 2002, 2, 0),
    "franco colapinto"      : (["williams","alpine"],                                                         "argentina",        0,   0, False, 2024, "", 2003, 1, 2024),
    "lance stroll"          : (["williams","racing point","aston martin"],                                   "canadiense",       0,   3, False, 2017, "", 1998, 8, 0),
    "kevin magnussen"       : (["mclaren","renault","haas"],                                                 "danesa",           0,   1, False, 2014, "mclaren", 1992, 1, 2024),
    "romain grosjean"       : (["renault","lotus","haas"],                                                   "francesa",         0,  10, False, 2009, "", 1986, 8, 2020),
    "mick schumacher"       : (["haas"],                                                                      "alemana",          0,   0, False, 2021, "ferrari", 1999, 2, 2022),
    "nico rosberg"          : (["williams","mercedes"],                                                       "alemana",         23,  57, 1, 2006, "", 1985, 10, 2016),
    "michael schumacher"    : (["jordan","benetton","ferrari","mercedes"],                                   "alemana",         91, 155, 7, 1991, "", 1969, 19, 2012),
    "juan manuel fangio"    : (["alfa romeo","maserati","mercedes","ferrari"],                               "argentina",       24,  35, 5, 1950, "", 1911, 8, 1958),
    "stirling moss"         : (["hwm","connaught","cooper","maserati","mercedes","vanwall","rob walker"],    "británica",       16,  24, False, 1951, "", 1929, 14, 1962),
    "mark webber"           : (["minardi","jaguar","williams","red bull"],                                   "australiana",      9,  42, False, 2002, "", 1976, 12, 2013),
    "david coulthard"       : (["williams","mclaren","red bull"],                                            "británica",       13,  62, False, 1994, "", 1971, 15, 2008),
    "yuki tsunoda"          : (["alphatauri","racing bulls","red bull"],                                      "japonesa",         0,   2, False, 2021, "red bull", 2000, 6, 0),
    "daniil kvyat"          : (["toro rosso","red bull","alphatauri"],                                       "rusa",             0,   3, False, 2014, "red bull", 1994, 7, 2021),
    "felipe massa"          : (["sauber","ferrari","williams"],                                              "brasileña",       11,  41, False, 2002, "ferrari", 1981, 15, 2017),
    "jenson button"         : (["williams","benetton","renault","bar","honda","brawn gp","mclaren"],         "británica",       15,  50, 1, 2000, "", 1980, 17, 2016),
    "rubens barrichello"    : (["jordan","stewart","ferrari","honda","brawn gp","williams"],                 "brasileña",       11,  68, False, 1993, "", 1972, 19, 2011),
    "rene arnoux"           : (["martini","surtees","renault","ferrari","ligier"],                           "francesa",         7,  22, False, 1978, "", 1948, 12, 1989),
    "giancarlo fisichella"  : (["minardi","jordan","benetton","sauber","renault","force india","ferrari"],   "italiana",         3,  19, False, 1996, "", 1973, 14, 2009),
    "jarno trulli"          : (["minardi","prost","jordan","renault","toyota","lotus"],                      "italiana",         1,  11, False, 1997, "", 1974, 13, 2011),
    "alain prost"           : (["mclaren","renault","ferrari","williams"],                                   "francesa",        51, 106, 4, 1980, "", 1955, 13, 1993),
    "nigel mansell"         : (["lotus","williams","ferrari","mclaren"],                                     "británica",       31,  59, 1, 1980, "", 1953, 15, 1995),
    "ayrton senna"          : (["toleman","lotus","mclaren","williams"],                                     "brasileña",       41,  80, 3, 1984, "", 1960, 10, 1994),
    "ralf schumacher"       : (["jordan","williams","toyota"],                                               "alemana",          6,  27, False, 1997, "", 1975, 11, 2007),
    "gerhard berger"        : (["ats","arrow","benetton","ferrari","mclaren"],                               "austriaca",       10,  48, False, 1984, "", 1959, 14, 1997),
    "riccardo patrese"      : (["shadow","arrows","brabham","williams","benetton"],                          "italiana",         6,  37, False, 1977, "", 1954, 17, 1993),
    "jackie stewart"        : (["brm","matra","tyrrell"],                                                    "británica",       27,  43, 3, 1965, "", 1939, 9, 1973),
    "juan pablo montoya"    : (["williams","mclaren"],                                                       "colombiana",       7,  30, False, 2001, "", 1975, 7, 2006),
    "pastor maldonado"      : (["williams","lotus"],                                                          "venezolana",       1,   1, False, 2011, "", 1985, 6, 2015),
    "robert kubica"         : (["bmw sauber","renault","williams","alfa romeo"],                              "polaca",           1,  12, False, 2006, "", 1984, 10, 2021),
    "heikki kovalainen"     : (["renault","mclaren","lotus","caterham"],                                     "finlandesa",       1,   4, False, 2007, "", 1981, 8, 2013),
    "nick heidfeld"         : (["prost","sauber","jordan","williams","bmw sauber","renault"],                "alemana",          0,  13, False, 2000, "", 1977, 10, 2011),
    "jacques villeneuve"    : (["williams","bar","renault","sauber","bmw sauber"],                           "canadiense",      11,  23, 1, 1996, "", 1971, 1, 0),
    "gilles villeneuve"     : (["mclaren","ferrari"],                                                        "canadiense",       6,  13, False, 1977, "ferrari", 1950, 5, 1982),
    "jean alesi"            : (["tyrrell","ferrari","benetton","sauber","jordan","prost"],                   "francesa",         1,  32, False, 1989, "ferrari", 1964, 13, 2001),
    "heinz-harold frentzen" : (["sauber","williams","jordan","prost","arrows"],                               "alemana",          3,  18, False, 1994, "", 1967, 11, 2003),
    "eddie irvine"          : (["jordan","ferrari","jaguar"],                                                 "británica",        4,  26, False, 1993, "ferrari", 1965, 8, 2002),
    "nelson piquet"         : (["brabham","williams","benetton","lotus"],                                     "brasileña",       23,  60, 3, 1978, "", 1952, 14, 1991),
    "emerson fittipaldi"    : (["lotus","mclaren","fittipaldi"],                                             "brasileña",       14,  35, 2, 1970, "", 1946, 11, 1980),
    "damon hill"            : (["brabham","williams","arrows","jordan"],                                      "británica",       22,  42, 1, 1992, "", 1960, 8, 1999),
    "mika hakkinen"         : (["lotus","mclaren"],                                                           "finlandesa",      20,  51, 2, 1991, "mclaren", 1968, 11, 2001),
    "jody scheckter"        : (["tyrrell","wolf","ferrari"],                                                  "sudafricana",     10,  33, 1, 1972, "", 1950, 1, 1980),
    "mario andretti"        : (["lotus","ferrari","alfa romeo","williams"],                                   "estadounidense",  12,  19, 1, 1968, "", 1940, 3, 1982),
    "james hunt"            : (["hesketh","mclaren","wolf"],                                                  "británica",       10,  23, 1, 1973, "", 1947, 8, 1979),
    "niki lauda"            : (["march","brm","ferrari","brabham","mclaren"],                                 "austriaca",       25,  54, 3, 1971, "ferrari", 1949, 14, 1985),
    "alan jones"            : (["hesketh","surtees","shadow","williams","arrows"],                            "australiana",     12,  24, 1, 1975, "", 1946, 8, 1986),
    "keke rosberg"          : (["wolf","fittipaldi","williams","lotus","mclaren"],                            "finlandesa",       5,  17, 1, 1978, "", 1948, 9, 1986),
    "vitaly petrov"         : (["renault","caterham"],                                                        "rusa",             0,   1, False, 2010, "", 1984, 3, 2012),
    "scott speed"           : (["toro rosso"],                                                                "estadounidense",   0,   0, False, 2006, "red bull", 1983, 2, 2007),
    "sebastien buemi"       : (["toro rosso"],                                                                "suiza",            0,   0, False, 2009, "red bull", 1988, 3, 2011),
    "jaime alguersuari"     : (["toro rosso"],                                                                "española",         0,   0, False, 2009, "red bull", 1990, 3, 2011),
    "jean-eric vergne"      : (["toro rosso"],                                                                "francesa",         0,   0, False, 2012, "red bull", 1990, 3, 2014),
    "sebastien bourdais"    : (["toro rosso"],                                                                "francesa",         0,   0, False, 2008, "", 1979, 1, 0),
    "brendon hartley"       : (["toro rosso"],                                                                "neozelandesa",     0,   0, False, 2017, "red bull", 1989, 2, 2018),
    "adrian sutil"          : (["spyker","force india","sauber"],                                             "alemana",          0,   0, False, 2007, "", 1983, 1, 0),
    "paul di resta"         : (["force india","williams"],                                                    "británica",        0,   0, False, 2011, "", 1986, 4, 2013),
    "thierry boutsen"       : (["arrows","benetton","williams","ligier","jordan"],                            "belga",            3,  15, False, 1983, "", 1957, 9, 1993),
    "martin brundle"        : (["tyrrell","zakspeed","williams","brabham","benetton","jordan","mclaren","ligier"], "británica",   0,   9, False, 1984, "", 1959, 9, 1996),
    "olivier panis"         : (["ligier","prost","bar","toyota"],                                             "francesa",         1,   5, False, 1994, "", 1966, 9, 2004),
    "alexander wurz"        : (["benetton","mclaren","williams"],                                             "austriaca",        0,   3, False, 1997, "", 1974, 6, 2007),
    "carlos reutemann"      : (["brabham","ferrari","lotus","williams"],                                      "argentina",       12,  45, False, 1972, "", 1942, 11, 1982),
    "clay regazzoni"        : (["ferrari","brm","ensign","shadow","williams","theodore"],                     "suiza",            5,  28, False, 1970, "", 1939, 11, 1980),
    "john watson"           : (["surtees","brabham","penske","mclaren","lotus"],                              "británica",        5,  20, False, 1973, "", 1946, 11, 1985),
    "nelson piquet jr"      : (["renault"],                                                                   "brasileña",        0,   0, False, 2008, "", 1985, 2, 2009),
    "mike hawthorn"         : (["cooper","ferrari","vanwall","brm","tyrrell"],                                "británica",        3,  18, 1, 1952, "", 1929, 1, 0),
    "peter collins"         : (["brm","vanwall","ferrari","maserati"],                                        "británica",        3,  11, False, 1952, "", 1931, 1, 0),
    "tony brooks"           : (["connaught","vanwall","ferrari","brm","cooper"],                              "británica",        6,  10, False, 1956, "", 1932, 1, 1961),
    "dan gurney"            : (["ferrari","brm","porsche","brabham","eagle"],                                 "estadounidense",   4,  19, False, 1959, "", 1931, 1, 1970),
    "john surtees"          : (["lotus","lola","ferrari","cooper","honda","brm"],                             "británica",        6,  24, 1, 1960, "ferrari", 1934, 1, 0),
    "jim clark"             : (["lotus"],                                                                      "británica",       25,  32, 2, 1960, "", 1936, 8, 1968),
    "graham hill"           : (["lotus","brm","brabham","embassy"],                                           "británica",       14,  36, 2, 1958, "", 1929, 18, 1975),
    "denny hulme"           : (["brabham","mclaren"],                                                         "neozelandesa",     8,  33, 1, 1965, "", 1936, 1, 1974),
    "jack brabham"          : (["cooper","lotus","brabham"],                                                   "australiana",    14,  31, 3, 1955, "", 1926, 16, 1970),
    "jochen rindt"          : (["cooper","brabham","lotus"],                                                   "austriaca",       6,  13, 1, 1964, "", 1942, 1, 1970),
    "giuseppe farina"       : (["alfa romeo","ferrari","maserati"],                                           "italiana",         5,  20, 1, 1950, "", 1906, 1, 1955),
    "alberto ascari"        : (["ferrari","maserati","lancia"],                                                "italiana",       13,  17, 2, 1950, "ferrari", 1918, 1, 1955),
    "piero taruffi"         : (["alfa romeo","ferrari","mercedes","maserati","vanwall"],                      "italiana",         1,   3, False, 1950, "ferrari", 1906, 1, 0),
    "derek warwick"         : (["toleman","renault","brabham","arrows","lotus","footwork"],                   "británica",        0,   4, False, 1981, "", 1954, 10, 1993),
    "takuma sato"           : (["bar","honda","super aguri","williams"],                                      "japonesa",         0,   1, False, 2002, "", 1977, 9, 2010),
    "timo glock"            : (["jordan","toyota","virgin"],                                                   "alemana",          0,   3, False, 2004, "", 1982, 6, 2016),
    "patrick tambay"        : (["surtees","theodore","mclaren","ligier","ferrari","renault"],                 "francesa",         2,  11, False, 1975, "ferrari", 1949, 6, 1986),
    "didier pironi"         : (["tyrrell","ligier","ferrari"],                                                 "francesa",         3,  13, False, 1978, "ferrari", 1952, 5, 1982),
    "ronnie peterson"       : (["march","tyrrell","lotus","brabham"],                                         "sueca",           10,  26, False, 1970, "", 1944, 11, 1978),
    "elio de angelis"       : (["shadow","lotus","brabham"],                                                   "italiana",         2,   8, False, 1980, "", 1958, 9, 1986),
    "francois cevert"       : (["tyrrell"],                                                                    "francesa",         1,  13, False, 1969, "", 1944, 6, 1973),
    "jochen mass"           : (["surtees","mclaren","arrows","mercedes"],                                     "alemana",          1,   8, False, 1973, "", 1946, 1, 0),
    "christijan albers"     : (["minardi","spyker"],                                                           "neerlandesa",      0,   0, False, 2005, "", 1979, 3, 2006),
    "vitantonio liuzzi"     : (["red bull","toro rosso","force india","hrt"],                                  "italiana",         0,   0, False, 2005, "red bull", 1981, 6, 2011),
    "narain karthikeyan"    : (["jordan","hrt"],                                                               "india",            0,   0, False, 2005, "", 1977, 5, 2012),
    "jo siffert"            : (["lotus","brm"],                                                                "suiza",            2,   5, False, 1962, "", 1936, 1, 1971),
    "pedro rodriguez"       : (["ferrari","brm","lotus"],                                                      "mexicana",         2,   7, False, 1963, "", 1940, 1, 1971),
    "jack doohan"           : (["alpine"],                                                                     "australiana",      0,   0, False, 2024, "alpine", 2003, 1, 0),
    "kimi antonelli"        : (["mercedes"],                                                                   "italiana",         0,   0, False, 2025, "mercedes", 2006, 1, 0),
    "isaac hadjar"          : (["racing bulls","red bull"],                                                    "francesa",         0,   0, False, 2025, "red bull", 2004, 1, 0),
    "arvid lindblad"        : (["racing bulls"],                                                               "sueca",            0,   0, False, 2025, "red bull", 2005, 1, 0),
    "christian klien"       : (["jaguar","red bull","hrt"],                                                    "austriaca",        0,   0, False, 2004, "red bull", 1983, 3, 2006),
    "tiago monteiro"        : (["jordan"],                                                                     "portuguesa",       0,   1, False, 2005, "", 1978, 3, 2006),
    "mika salo"             : (["lotus","tyrrell","arrows","ferrari","toyota"],                                "finlandesa",       0,   3, False, 1994, "ferrari", 1966, 8, 2002),
    "andrea de cesaris"     : (["alfa romeo","mclaren","ligier","minardi","brabham","rial","dallara","jordan","tyrrell","sauber"], "italiana", 0, 5, False, 1980, "", 0, 14, 1994),
    "chris amon"            : (["lotus","ferrari","march","tyrrell","matra"],                                  "neozelandesa",     0,  11, False, 1963, "ferrari", 1943, 1, 0),
    "jean pierre jabouille" : (["williams","surtees","tyrell","renault","ligier"],                             "francesa",         2,   3, False, 1975, "", 1942, 1, 0),
    "esteban gutierrez"     : (["sauber","haas"],                                                              "mexicana",         0,   0, False, 2012, "ferrari", 1991, 1, 0),
    "nikita mazepin"        : (["haas"],                                                                       "rusa",             0,   0, False, 2021, "", 1999, 1, 2021),
    "pietro fittipaldi"     : (["haas"],                                                                       "brasileña",        0,   0, False, 2020, "", 1996, 1, 2020),
    "lucas di grassi"       : (["virgin"],                                                                     "brasileña",        0,   0, False, 2010, "", 1984, 1, 0),
    # ── Pilotos F1 adicionales ────────────────────────────────────
    "stefan johansson"      : (["spirit","tyrrell","ferrari","mclaren","ligier","onyx"],                         "sueca",            0,  12, False, 1983, "ferrari", 1956, 1, 1991),
    "michele alboreto"      : (["tyrrell","ferrari","lola","footwork","minardi","arrows"],                       "italiana",         5,  23, False, 1981, "ferrari", 1956, 1, 1994),
    "teo fabi"              : (["toleman","brabham","benetton"],                                                  "italiana",         0,   3, False, 1982, "", 1955, 1, 0),
    "marc surer"            : (["ensign","ats","arrows","brabham"],                                               "suiza",            0,   6, False, 1979, "", 1951, 1, 0),
    "ivan capelli"          : (["march","ferrari"],                                                               "italiana",         0,   7, False, 1985, "ferrari", 1963, 1, 1993),
    "pierluigi martini"     : (["minardi","scuderia italia","ferrari"],                                           "italiana",         0,   0, False, 1985, "ferrari", 1961, 1, 0),
    "alex caffi"            : (["osella","dallara","arrows","footwork"],                                          "italiana",         0,   1, False, 1986, "", 1964, 1, 0),
    "aguri suzuki"          : (["lola","larrousse","footwork","jordan"],                                          "japonesa",         0,   1, False, 1988, "", 1960, 1, 0),
    "satoru nakajima"       : (["lotus","tyrrell"],                                                               "japonesa",         0,   1, False, 1987, "", 1953, 1, 0),
    "ukyo katayama"         : (["tyrrell"],                                                                       "japonesa",         0,   0, False, 1992, "", 1963, 1, 0),
    "taki inoue"            : (["simtek","footwork"],                                                             "japonesa",         0,   0, False, 1994, "", 1963, 1, 0),
    "shinji nakano"         : (["prost","minardi"],                                                               "japonesa",         0,   0, False, 1997, "", 1971, 1, 0),
    "kamui kobayashi"       : (["toyota","sauber","caterham"],                                                    "japonesa",         0,   3, False, 2009, "", 1986, 6, 2014),
    "jos verstappen"        : (["benetton","simtek","footwork","tyrrell","stewart","arrows","minardi"],           "neerlandesa",      0,   2, False, 1994, "", 1972, 8, 2003),
    "giedo van der garde"   : (["caterham"],                                                                      "neerlandesa",      0,   0, False, 2013, "sauber", 1985, 1, 0),
    "robert doornbos"       : (["minardi","red bull"],                                                            "neerlandesa",      0,   0, False, 2005, "red bull", 1981, 1, 0),
    "pedro de la rosa"      : (["arrows","jaguar","mclaren","sauber","hrt"],                                      "española",         0,   0, False, 1999, "mclaren", 1971, 9, 2012),
    "marc gene"             : (["minardi","williams","ferrari"],                                                   "española",         0,   0, False, 1999, "ferrari", 1974, 3, 2004),
    "roberto merhi"         : (["manor","marussia"],                                                              "española",         0,   0, False, 2015, "", 1991, 1, 2015),
    "hector rebaque"        : (["brabham","lotus"],                                                               "mexicana",         0,   0, False, 1977, "", 1956, 1, 0),
    "christian fittipaldi"  : (["minardi","footwork"],                                                            "brasileña",        0,   0, False, 1992, "", 1971, 3, 1994),
    "pedro paulo diniz"     : (["forti","ligier","arrows","sauber"],                                              "brasileña",        0,   0, False, 1995, "", 1970, 5, 0),
    "antonio pizzonia"      : (["jaguar","williams","bmw sauber"],                                                "brasileña",        0,   0, False, 2003, "", 1980, 2, 2005),
    "enrique bernoldi"      : (["arrows"],                                                                        "brasileña",        0,   0, False, 2001, "", 1978, 2, 0),
    "tarso marques"         : (["minardi"],                                                                       "brasileña",        0,   0, False, 1996, "", 1976, 3, 0),
    "erik comas"            : (["ligier","larrousse"],                                                            "francesa",         0,   3, False, 1991, "", 1963, 1, 0),
    "jean-marc gounon"      : (["minardi","simtek"],                                                              "francesa",         0,   0, False, 1993, "", 1963, 1, 0),
    "charles pic"           : (["marussia","caterham"],                                                           "francesa",         0,   0, False, 2012, "", 1990, 2, 2013),
    "jules bianchi"         : (["marussia"],                                                                      "francesa",         0,   2, False, 2013, "ferrari", 1989, 2, 2014),
    "luca badoer"           : (["scuderia italia","minardi","ferrari"],                                           "italiana",         0,   0, False, 1993, "ferrari", 1971, 1, 2009),
    "antonio giovinazzi"    : (["sauber","alfa romeo"],                                                           "italiana",         0,   3, False, 2017, "ferrari", 1993, 4, 2021),
    "guanyu zhou"           : (["alfa romeo"],                                                                    "china",            0,   0, False, 2022, "sauber", 1999, 3, 2024),
    "nyck de vries"         : (["williams","alphatauri"],                                                         "neerlandesa",      0,   0, False, 2022, "mercedes", 1995, 1, 2023),
    "stoffel vandoorne"     : (["mclaren"],                                                                       "belga",            0,   0, False, 2016, "mclaren", 1992, 2, 2018),
    "pascal wehrlein"       : (["manor","sauber"],                                                                "alemana",          0,   0, False, 2016, "mercedes", 1994, 2, 2017),
    "rio haryanto"          : (["manor"],                                                                         "indonesia",        0,   0, False, 2016, "", 1993, 1, 2016),
    "max chilton"           : (["marussia"],                                                                      "británica",        0,   0, False, 2013, "", 1991, 2, 2014),
    "will stevens"          : (["caterham","manor"],                                                              "británica",        0,   0, False, 2014, "", 1991, 2, 2015),
    "jordan king"           : (["manor"],                                                                         "británica",        0,   0, False, 2016, "", 1994, 1, 0),
    "alexander rossi"       : (["marussia"],                                                                      "estadounidense",   0,   0, False, 2015, "", 1991, 1, 2015),
    "logan sargeant"        : (["williams"],                                                                      "estadounidense",   0,   0, False, 2023, "williams", 2000, 1, 2024),
    "sakon yamamoto"        : (["super aguri","spyker"],                                                          "japonesa",         0,   0, False, 2006, "", 1982, 1, 0),
    "markus winkelhock"     : (["spyker"],                                                                        "alemana",          0,   0, False, 2007, "", 1980, 1, 0),
    "anthony davidson"      : (["bar","super aguri","honda"],                                                     "británica",        0,   0, False, 2002, "", 1979, 1, 0),
    "nicholas latifi"       : (["williams"],                                                                      "canadiense",       0,   0, False, 2020, "", 1995, 1, 2022),
    "patrick depailler"     : (["tyrrell","ligier","alfa romeo"],                                                  "francesa",         2,   9, False, 1972, "", 1944, 7, 0),
    "eddie cheever"         : (["theodore","hesketh","osella","tyrrell","ligier","renault","alfa romeo","arrows"], "estadounidense",   0,   9, False, 1978, "", 1958, 11, 1989),
    "jose froilan gonzalez" : (["maserati","ferrari"],                                                             "argentina",        2,   7, False, 1950, "", 1922, 1, 1957),
    "zsolt baumgartner"     : (["jordan","minardi"],                                                               "húngara",          0,   0, False, 2003, "", 1981, 2, 2004),
    "ralph firman"          : (["jordan"],                                                                         "irlandesa",        0,   0, False, 2003, "", 1980, 1, 2003),
    "bruno senna"           : (["hrt","renault","williams"],                                                       "brasileña",        0,   0, False, 2010, "", 1983, 1, 2012),
    "nick de vries"         : (["williams","alphatauri"],                                                          "neerlandesa",      0,   0, False, 2022, "", 1995, 1, 0),
    "stefan bellof"         : (["tyrrell"],                                                                        "alemana",          0,   0, False, 1984, "", 1957, 1, 0),
    "Jacques villeneuve"    : (["williams","bar","renault","sauber","bmw sauber"],                                 "canadiense",      11,  23, 1, 1996, "", 1971, 1, 0),
    "luigi fagioli"         : (["alfa romeo"],                                                                     "italiana",         1,   3, False, 1950, "", 1898, 1, 0),

    # ── Pilotos añadidos: Años 50-60 ─────────────────────────────
    "luigi musso"           : (["maserati","ferrari"],                                                               "italiana",         3,   7, False, 1953, "", 1924, 5, 1958),
    "roy salvadori"         : (["connaught","maserati","cooper","aston martin","lola"],                              "británica",        0,   3, False, 1952, "", 1922, 8, 1962),
    "harry schell"          : (["gordini","maserati","vanwall","bra","cooper"],                                      "estadounidense",   0,   3, False, 1950, "", 1921, 8, 1959),
    "wolfgang von trips"    : (["ferrari"],                                                                          "alemana",          2,  10, False, 1956, "", 1928, 5, 1961),
    "tony brooks"           : (["bra","vanwall","ferrari","cooper","bra"],                                           "británica",        6,  10, False, 1956, "", 1932, 6, 1961),
    "richie ginther"        : (["ferrari","bra","cooper","honda"],                                                   "estadounidense",   1,  14, False, 1960, "", 1930, 8, 1967),
    "innes ireland"         : (["lotus","british racing partnership","lola"],                                        "británica",        1,   3, False, 1959, "", 1930, 6, 1966),
    "jack fairman"          : (["connaught","cooper","bra"],                                                         "británica",        0,   0, False, 1953, "", 1913, 4, 1961),
    "bruce mclaren"         : (["cooper","bruce mclaren motor racing"],                                              "neozelandesa",     4,  27, False, 1958, "", 1937, 9, 1970),
    "jo bonnier"            : (["bra","maserati","bra","cooper","honda","brabham"],                                  "sueca",            1,   3, False, 1956, "", 1930, 10, 1971),
    "lorenzo bandini"       : (["cooper","ferrari"],                                                                 "italiana",         1,  10, False, 1961, "", 1935, 6, 1967),
    "giancarlo baghetti"    : (["ferrari","ats","centro sud"],                                                       "italiana",         1,   1, False, 1961, "", 1934, 5, 1967),
    "trevor taylor"         : (["lotus","bra"],                                                                      "británica",        0,   1, False, 1961, "", 1936, 3, 1966),
    "bob anderson"          : (["dw racing"],                                                                        "británica",        0,   0, False, 1963, "", 1931, 4, 1967),
    "mike spence"           : (["lotus","brm"],                                                                      "británica",        0,   3, False, 1963, "", 1936, 5, 1968),
    "piers courage"         : (["brm","frank williams","de tomaso"],                                                 "británica",        0,   4, False, 1966, "", 1942, 4, 1970),

    # ── Pilotos añadidos: Años 70-80 ─────────────────────────────
    "hans joachim stuck"    : (["march","brabham","shadow","ats","williams"],                                        "alemana",          0,   3, False, 1974, "", 1951, 7, 1987),
    "arturo merzario"       : (["ferrari","iso marlboro","williams","wolf williams","fittipaldi","arrow"],           "italiana",         0,   1, False, 1972, "", 1943, 5, 1979),
    "helmut marko"          : (["brm"],                                                                              "austriaca",        0,   0, False, 1971, "", 1943, 1, 1972),
    "emilio de villota"     : (["williams","march","fittipaldi"],                                                    "española",         0,   0, False, 1977, "", 1946, 2, 1982),
    "bruno giacomelli"      : (["mclaren","alfa romeo","toleman"],                                                   "italiana",         0,   1, False, 1977, "", 1952, 6, 1983),
    "jean pierre beltoise"  : (["matra","brm"],                                                                      "francesa",         1,  11, False, 1968, "", 1937, 9, 1974),
    "howden ganley"         : (["brm","iso","williams","march","maki"],                                              "neozelandesa",     0,   0, False, 1971, "", 1941, 3, 1974),
    "henri pescarolo"       : (["matra","brm","march","surtees","williams"],                                         "francesa",         0,   1, False, 1968, "", 1942, 6, 1976),
    "francois cevert"       : (["tyrrell"],                                                                          "francesa",         1,  13, False, 1969, "", 1944, 5, 1973),
    "vittorio brambilla"    : (["march","surtees","alfa romeo"],                                                     "italiana",         1,   1, False, 1974, "", 1937, 7, 1980),
    "lella lombardi"        : (["march","williams","brabham"],                                                       "italiana",         0,   1, False, 1974, "", 1941, 3, 1976),
    "torsten palm"          : (["hesketh"],                                                                           "sueca",            0,   0, False, 1975, "", 1947, 1, 1975),
    "gunnar nilsson"        : (["lotus"],                                                                             "sueca",            1,   2, False, 1976, "", 1948, 2, 1977),
    "jochen mass"           : (["surtees","mclaren","wolf","arrows","march"],                                        "alemana",          1,   5, False, 1973, "", 1946, 9, 1982),
    "clay regazzoni"        : (["ferrari","brm","ensign","williams","brabham"],                                      "suiza",            5,  28, False, 1970, "", 1939, 11, 1980),
    "hector rebaque"        : (["hesketh","lotus","brabham"],                                                        "mexicana",         0,   0, False, 1977, "", 1956, 5, 1981),
    "jan lammers"           : (["shadow","ensign","ats","arrows"],                                                   "neerlandesa",      0,   0, False, 1979, "", 1956, 3, 1992),
    "marc surer"            : (["ensign","ats","theodore","arrows","brabham"],                                       "suiza",            0,   5, False, 1979, "", 1951, 8, 1986),
    "kenny acheson"         : (["ram","tyrrell"],                                                                    "irlandesa",        0,   0, False, 1983, "", 1957, 2, 1985),
    "jonathan palmer"       : (["ram","zakspeed","tyrrell"],                                                         "británica",        0,   0, False, 1983, "", 1956, 5, 1989),
    "christian danner"      : (["zakspeed","arrows","rial"],                                                         "alemana",          0,   0, False, 1985, "", 1958, 4, 1989),
    "philippe alliot"       : (["ram","larrousse","ligier"],                                                         "francesa",         0,   0, False, 1984, "", 1954, 7, 1994),
    "yannick dalmas"        : (["larrousse","ags","coloni"],                                                         "francesa",         0,   0, False, 1987, "", 1961, 3, 1994),
    "bertrand gachot"       : (["onyx","coloni","jordan","larrousse","pacific"],                                     "belga",            0,   1, False, 1989, "", 1962, 5, 1995),
    "mika salo"             : (["lotus","tyrrell","arrows","baa","sauber","toyota","ferrari"],                       "finlandesa",       0,   6, False, 1994, "", 1966, 8, 2002),
    "jj lehto"              : (["onyx","dallara","sauber","benetton","sauber"],                                       "finlandesa",       0,   3, False, 1989, "", 1966, 5, 1994),
    "johnny herbert"        : (["benetton","lotus","ligier","sauber","stewart","jaguar"],                             "británica",        3,   8, False, 1989, "", 1964, 9, 2000),
    "johnny cecotto"        : (["toleman"],                                                                            "venezolana",       0,   0, False, 1983, "", 1956, 1, 1984),
    "heikki kovalainen"     : (["renault","mclaren","lotus","caterham"],                                              "finlandesa",       1,   4, False, 2007, "", 1981, 7, 2013),
    "tarso marques"         : (["minardi"],                                                                            "brasileña",        0,   0, False, 1996, "", 1975, 2, 2001),
    "luca badoer"           : (["footwork","minardi","ferrari"],                                                       "italiana",         0,   0, False, 1993, "", 1971, 5, 2009),
    "ivan capelli"          : (["tyrrell","march","leyton house","ferrari","jordan"],                                  "italiana",         0,   3, False, 1985, "", 1963, 8, 1993),
}

# ══════════════════════════════════════════════════════════════════
#  BASE DE DATOS — FÓRMULA 2
#  (equipos, nacionalidad, victorias_f2, podios_f2, campeón_f2)
#  Equipos = escuderías de F2 donde corrió
#  Victorias/podios = en F2
#  Campeón = campeón de F2/GP2
# ══════════════════════════════════════════════════════════════════
RAW_F2 = {
    # ── Campeones F2/GP2 ──────────────────────────────────────────
    "nico rosberg"          : (["asm"],                                                                        "alemana",          4,   9, 1, 2005, "", 1985, 2, 2005),     # GP2 2005),
    "lewis hamilton"        : (["art"],                                                                        "británica",        5,  12, 7, 2006, "mclaren", 1985, 1, 2006),     # GP2 2006),
    "timo glock"            : (["isport"],                                                                     "alemana",          4,   8, True, 2007, "", 1982, 1, 2007),     # GP2 2007
    "giorgio pantano"       : (["racing engineering"],                                                         "italiana",         5,  10, True, 2008, "", 1979, 1, 2008),     # GP2 2008
    "nico hulkenberg"       : (["art"],                                                                        "alemana",          7,  14, True, 2009, "", 1987, 1, 2009),     # GP2 2009
    "pastor maldonado"      : (["rapax"],                                                                      "venezolana",       7,  14, True, 2010, "", 1985, 1, 2010),     # GP2 2010
    "romain grosjean"       : (["dams"],                                                                       "francesa",         9,  17, True, 2011, "", 1986, 1, 2011),     # GP2 2011
    "davide valsecchi"      : (["dams"],                                                                       "italiana",         7,  12, True, 2012, "", 1985, 1, 2012),     # GP2 2012
    "fabio leimer"          : (["racing engineering"],                                                         "suiza",            4,   9, True, 2013, "", 1989, 1, 2013),     # GP2 2013
    "jolyon palmer"         : (["dams"],                                                                        "británica",        7,  12, True, 2014, "", 1991, 1, 2014),     # GP2 2014
    "stoffel vandoorne"     : (["art"],                                                                        "belga",            7,  16, True, 2015, "mclaren", 1992, 1, 2015),     # GP2 2015
    "pierre gasly"          : (["prema"],                                                                       "francesa",         5,  10, True, 2016, "", 1996, 2, 2016),     # GP2 2016
    "charles leclerc"       : (["prema"],                                                                       "monegasca",       13,  21, True, 2017, "ferrari", 1997, 2, 2017),     # F2 2017
    "george russell"        : (["art"],                                                                        "británica",         7,  14, True, 2018, "mercedes", 1998, 2, 2018),     # F2 2018
    "nyck de vries"         : (["art"],                                                                        "neerlandesa",      9,  15, True, 2019, "mercedes", 1995, 3, 2019),     # F2 2019
    "mick schumacher"       : (["prema"],                                                                       "alemana",          5,  10, True, 2020, "ferrari", 1999, 2, 2020),     # F2 2020
    "oscar piastri"         : (["prema"],                                                                       "australiana",     10,  17, True, 2021, "alpine", 2001, 2, 2021),     # F2 2021
    "felipe drugovich"      : (["mp motorsport"],                                                              "brasileña",        7,  14, True, 2022, "alpine", 1998, 1, 2022),     # F2 2022
    "theo pourchaire"       : (["art"],                                                                        "francesa",         5,  10, True, 2023, "sauber", 2003, 3, 2023),     # F2 2023

    # ── Pilotos destacados que pasaron por F2 ────────────────────
    "lando norris"          : (["carlin"],                                                                     "británica",         5,  13, False, 2018, "mclaren", 1999, 1, 2018),
    "alex albon"            : (["art"],                                                                        "tailandesa",        4,  10, False, 2018, "red bull", 1996, 1, 2018),
    "nicholas latifi"       : (["dams"],                                                                       "canadiense",        4,  11, False, 2019, "", 1995, 3, 0),
    "jack aitken"           : (["campos","carlin"],                                                            "británica",         2,   5, False, 2019, "", 1995, 2, 2020),
    "luca ghiotto"          : (["russian time","campos","hitech","virtuosi"],                                  "italiana",          8,  22, False, 2016, "", 1992, 5, 2020),
    "artem markelov"        : (["russian time"],                                                               "rusa",              4,  12, False, 2016, "", 1994, 4, 2019),
    "sergio sette camara"   : (["dams","mp motorsport"],                                                       "brasileña",         3,   8, False, 2017, "red bull", 1996, 2, 2018),
    "nobuharu matsushita"   : (["art","carlin","mp motorsport"],                                               "japonesa",          4,   9, False, 2016, "mclaren", 1993, 4, 2019),
    "jordan king"           : (["mp motorsport"],                                                              "británica",         0,   1, False, 2016, "", 1994, 2, 0),
    "roberto merhi"         : (["campos"],                                                                     "española",          1,   2, False, 2014, "", 1991, 2, 0),
    "antonio fuoco"         : (["prema","charouz"],                                                            "italiana",          2,   5, False, 2017, "ferrari", 1996, 2, 2018),
    "santino ferrucci"      : (["trident"],                                                                    "estadounidense",    1,   3, False, 2018, "haas", 1998, 2, 0),
    "tadasuke makino"       : (["campos"],                                                                     "japonesa",          0,   0, False, 2018, "", 0, 1, 0),
    "maximilian gunther"    : (["campos","carlin","arden","trident","prema"],                                  "alemana",           2,   7, False, 2017, "", 1997, 4, 2020),
    "callum ilott"          : (["sauber junior","virtuosi"],                                                   "británica",         4,  10, False, 2019, "ferrari", 1998, 2, 2021),
    "yuki tsunoda"          : (["carlin"],                                                                     "japonesa",          3,   9, False, 2020, "red bull", 2000, 1, 2020),
    "christian lundgaard"   : (["art"],                                                                        "danesa",            1,   4, False, 2020, "alpine", 2001, 2, 0),
    "guanyu zhou"           : (["virtuosi","uni-virtuosi"],                                                    "china",             5,  15, False, 2020, "alpine", 1999, 3, 2022),
    "dan ticktum"           : (["dams","carlin"],                                                              "británica",         2,   5, False, 2020, "red bull", 1999, 2, 2021),
    "juri vips"             : (["hitech"],                                                                     "estonia",           2,   4, False, 2021, "red bull", 2000, 2, 2022),
    "marcus armstrong"      : (["art","dams","hitech"],                                                        "neozelandesa",      2,   5, False, 2020, "ferrari", 2000, 3, 2022),
    "dennis hauger"         : (["prema"],                                                                       "noruega",           5,  10, False, 2022, "red bull", 2002, 2, 2023),
    "jehan daruvala"        : (["carlin","prema"],                                                             "india",             5,  11, False, 2020, "red bull", 1999, 3, 2022),
    "ayumu iwasa"           : (["dams","hitech"],                                                              "japonesa",          3,   7, False, 2022, "red bull", 2002, 2, 2023),
    "gabriel bortoleto"     : (["invicta","carlin"],                                                           "brasileña",         8,  13, False, 2024, "mclaren", 2004, 1, 2024),
    "franco colapinto"      : (["mp motorsport"],                                                              "argentina",         2,   5, False, 2023, "williams", 2003, 1, 2023),
    "roman stanek"          : (["trident","invicta"],                                                          "checa",             1,   3, False, 2022, "", 2002, 1, 0),
    "sebastien buemi"       : (["arden"],                                                                      "suiza",             0,   1, False, 2008, "red bull", 1988, 2, 2008),
    "pedro piquet"          : (["trident","charouz","van amersfoort"],                                         "brasileña",         0,   0, False, 2020, "", 2000, 2, 2021),
    "ralph boschung"        : (["campos","carlin","charouz"],                                                  "suiza",             0,   1, False, 2019, "", 1997, 3, 2023),
    "jake dennis"           : (["arden","carlin"],                                                             "británica",         0,   1, False, 2018, "red bull", 1995, 1, 2019),
    "marino sato"           : (["trident","dams"],                                                             "japonesa",          0,   0, False, 2021, "", 1997, 2, 2023),
    "giuliano alesi"        : (["trident","charouz"],                                                          "francesa",          0,   1, False, 2020, "ferrari", 1999, 1, 2021),
    "calan williams"        : (["campos"],                                                                     "australiana",       0,   0, False, 2021, "", 2000, 3, 0),
    "clement novalak"       : (["campos","trident","mp motorsport"],                                           "francesa",          0,   2, False, 2021, "", 1999, 2, 2023),
    "enzo fittipaldi"       : (["charouz","carlin"],                                                           "brasileña",         0,   1, False, 2021, "haas", 2000, 3, 2024),
    "alex palou"            : (["campos"],                                                                     "española",          0,   0, False, 2019, "", 1997, 1, 0),
    "arthur leclerc"        : (["charouz","dams"],                                                             "monegasca",         1,   3, False, 2022, "ferrari", 2000, 1, 0),
    "amaury cordeel"        : (["van amersfoort","campos"],                                                    "belga",             0,   0, False, 2022, "", 2000, 2, 2023),
    "cem bolukbasi"         : (["charouz"],                                                                     "turca",             0,   0, False, 2022, "sauber", 1999, 1, 0),
    "david beckmann"        : (["charouz","campos"],                                                           "alemana",           0,   0, False, 2021, "", 2000, 2, 2021),
    "liam lawson"           : (["hitech","carlin","mp motorsport"],                                            "neozelandesa",      5,  10, False, 2021, "red bull", 2002, 3, 2023),
    "jack doohan"           : (["virtuosi"],                                                                    "australiana",       2,   5, False, 2023, "alpine", 2003, 2, 2024),
    "sebastien ogier"       : (["carlin"],                                                                     "francesa",          0,   0, False, 2022, "", 2001, 1, 0),
    "brendon hartley"       : (["ocean racing"],                                                               "neozelandesa",      0,   0, False, 2012, "red bull", 1989, 2, 2013),
    "antonio giovinazzi"    : (["prema"],                                                                       "italiana",          6,  13, False, 2016, "ferrari", 1993, 2, 0),
    "sean gelael"           : (["prema","dams"],                                                               "indonesia",         0,   2, False, 2017, "red bull", 1996, 3, 2020),
    "mahaveer raghunathan"  : (["mp motorsport"],                                                              "india",             0,   0, False, 2019, "", 1996, 1, 0),
    "tatiana calderon"      : (["charouz"],                                                                     "colombiana",        0,   0, False, 2019, "sauber", 1993, 1, 0),
    "giulio moises"         : (["campos"],                                                                     "ecuatoriana",       0,   0, False, 2021, "ferrari", 1998, 1, 0),
    "robert shwartzman"     : (["prema","dams"],                                                               "rusa",              5,  12, False, 2020, "ferrari", 1999, 3, 2023),
    "correa"                : (["sauber junior"],                                                              "estadounidense",    0,   2, False, 2019, "ferrari", 1999, 1, 0),
    # ── Pilotos F2 adicionales ────────────────────────────────────
    "gianluca petecof"      : (["prema","campos"],                                                               "brasileña",        2,   5, False, 2021, "ferrari", 2001, 2, 2022),
    "niko kari"             : (["trident","mp motorsport"],                                                      "finlandesa",       0,   1, False, 2018, "", 1998, 1, 0),
    "nikita mazepin"        : (["art"],                                                                           "rusa",             1,   2, False, 2019, "", 1999, 2, 0),
    "caio collet"           : (["mp motorsport"],                                                                 "brasileña",        2,   4, False, 2022, "alpine", 2001, 3, 0),

    # ── F2 adicionales 2023-2025 ──────────────────────────────────
    "andrea kimi antonelli" : (["prema"],                                                                         "italiana",         7,  15, True,  2024, "mercedes", 2006, 2, 2024),
    "oliver bearman"        : (["prema"],                                                                         "británica",        3,   7, False, 2023, "ferrari",  2005, 2, 2024),
    "isack hadjar"          : (["hitech","prema"],                                                                "francesa",         4,  10, True,  2024, "red bull", 2004, 2, 2024),
    "paul aron"             : (["hitech","dams"],                                                                  "estonia",          2,   6, False, 2023, "ferrari",  2003, 2, 2024),
    "oliver goethe"         : (["campos"],                                                                        "alemana",          1,   3, False, 2024, "",         2003, 1, 2024),
    "pepe marti"            : (["campos"],                                                                        "española",         1,   2, False, 2024, "ferrari",  2004, 1, 2024),
    "kush maini"            : (["invicta","mp motorsport"],                                                       "india",            2,   5, False, 2022, "",         2000, 3, 0),
    "richard verschoor"     : (["mp motorsport","trident"],                                                       "neerlandesa",      3,   8, False, 2021, "",         2000, 3, 0),
    "zak o'sullivan"        : (["prema","art"],                                                                   "británica",        3,   7, False, 2023, "mercedes", 2003, 2, 0),
    "jake hughes"           : (["hitech","dams"],                                                                  "británica",        3,   6, False, 2020, "mercedes", 1996, 4, 0),
    "victor martins"        : (["art","mp motorsport"],                                                           "francesa",         4,  10, False, 2022, "alpine",   2002, 3, 0),
    "frederik vesti"        : (["art","prema"],                                                                   "danesa",           4,   9, False, 2022, "mercedes", 2002, 3, 0),
    "jak crawford"          : (["hitech","dams"],                                                                  "estadounidense",   2,   5, False, 2022, "red bull", 2003, 3, 0),
    "juan manuel correa"    : (["sauber junior","art"],                                                           "ecuatoriana",      1,   3, False, 2019, "ferrari",  1999, 3, 0),
    "dino beganovic"        : (["prema"],                                                                         "sueca",            1,   3, False, 2023, "ferrari",  2003, 2, 0),
    "ryan lim"              : (["rodin"],                                                                          "singapurense",     0,   0, False, 2025, "",         2004, 1, 0),

    # ── F2 campeones históricos y pilotos 2024-2025 ───────────────
    "nelson piquet jr"      : (["piquet sports"],                                                                  "brasileña",        3,   8, True,  2008, "", 1985, 2, 2008),
    "vitaly petrov"         : (["barwa addax"],                                                                    "rusa",             4,   9, True,  2009, "", 1984, 1, 2009),
    "nico muller"           : (["rapax","arden"],                                                                  "suiza",            3,   7, False, 2013, "", 1992, 2, 0),
    "sean gelael"           : (["campos","prema","dams"],                                                          "indonesia",        0,   1, False, 2015, "red bull", 1996, 4, 0),
    "luca ghiotto"          : (["russian time","uni-virtuosi"],                                                    "italiana",         8,  17, False, 2015, "", 1992, 5, 0),
    "artem markelov"        : (["russian time"],                                                                   "rusa",             7,  16, False, 2015, "", 1994, 4, 0),
    "jack aitken"           : (["campos","arden","hitech"],                                                        "británica",        1,   5, False, 2017, "renault", 1995, 3, 0),
    "nobuharu matsushita"   : (["art","carlin","mp motorsport"],                                                   "japonesa",         5,  11, False, 2015, "honda", 1993, 5, 0),
    "tadasuke makino"       : (["carlin"],                                                                         "japonesa",         0,   1, False, 2018, "honda", 1997, 1, 0),
    "santino ferrucci"      : (["trident","dams"],                                                                 "estadounidense",   0,   2, False, 2017, "ferrari", 1998, 2, 0),
    "jordan king"           : (["mp motorsport","racing engineering"],                                             "británica",        0,   1, False, 2016, "", 1994, 2, 0),
    "ralph boschung"        : (["jenzer","campos"],                                                                "suiza",            1,   2, False, 2019, "", 1997, 4, 0),
    "cem bolukbasi"         : (["charouz"],                                                                        "turca",            0,   0, False, 2022, "", 2000, 1, 0),
    "mahaveer raghunathan"  : (["mp motorsport"],                                                                  "india",            0,   0, False, 2019, "", 1999, 1, 0),
    "joshua duerksen"       : (["charouz"],                                                                        "paraguaya",        0,   0, False, 2021, "", 1999, 1, 0),
    "amaury cordeel"        : (["van amersfoort","campos"],                                                        "belga",            0,   0, False, 2022, "", 2000, 2, 0),
    "roberto merhi"         : (["rapax","campos"],                                                                 "española",         0,   1, False, 2013, "", 1991, 3, 0),
    "jehan daruvala"        : (["carlin","prema"],                                                                 "india",            6,  13, False, 2019, "red bull", 1998, 3, 0),
    "dennis hauger"         : (["prema","mp motorsport"],                                                          "noruega",          4,   9, False, 2022, "red bull", 2002, 3, 0),
    "christian lundgaard"   : (["art"],                                                                            "danesa",           3,   7, False, 2021, "alpine", 2001, 1, 0),
    "brendon hartley"       : (["coloni","tech 1"],                                                                "neozelandesa",     0,   1, False, 2012, "red bull", 1989, 2, 0),
    "callum ilott"          : (["sauber junior","virtuosi"],                                                       "británica",        3,   9, False, 2019, "ferrari", 1998, 2, 0),
    "ayumu iwasa"           : (["dams","hitech"],                                                                  "japonesa",         3,   7, False, 2022, "red bull", 2001, 3, 0),
    "roman stanek"          : (["trident","hitech"],                                                               "checa",            1,   3, False, 2022, "",         2002, 3, 0),
    "arthur leclerc"        : (["dams","prema"],                                                                   "monegasca",        2,   6, False, 2022, "ferrari",  2000, 3, 0),
    "enzo fittipaldi"       : (["charouz","carlin"],                                                               "brasileña",        1,   3, False, 2021, "haas",     2000, 3, 0),
    "calan williams"        : (["campos","trident","prema"],                                                       "australiana",      0,   1, False, 2021, "",         2000, 3, 0),
    "juri vips"             : (["hitech","dams"],                                                                  "estonia",          3,   7, False, 2021, "red bull", 2000, 3, 0),
    "marcus armstrong"      : (["art","dams","hitech"],                                                            "neozelandesa",     3,   8, False, 2020, "ferrari",  2000, 3, 0),
    "dan ticktum"           : (["dams","carlin"],                                                                  "británica",        4,   8, False, 2020, "red bull", 1999, 2, 0),
    "giuliano alesi"        : (["trident","hitech"],                                                               "francesa",         0,   1, False, 2019, "ferrari",  1999, 3, 0),
    "nicholas latifi"       : (["dams"],                                                                           "canadiense",       3,   9, False, 2018, "",         1995, 3, 2018),
}

# ══════════════════════════════════════════════════════════════════
#  CLASE DE SERIE — encapsula toda la lógica de una categoría
# ══════════════════════════════════════════════════════════════════
class Series:
    def __init__(self, name, raw_data, champion_label, popular_teams):
        self.name            = name
        self.champion_label  = champion_label   # "Campeón del Mundo" o "Campeón de F2"
        self.popular_teams   = popular_teams

        # Construir meta
        self.drivers_meta = {}
        self.drivers_data = {}
        for drv, (teams, nat, wins, pods, champ, debut, academy, birth_year, seasons, last_season) in raw_data.items():
            self.drivers_meta[drv] = {
                "teams"      : teams,
                "nationality": nat,
                "wins"       : wins,
                "podiums"    : pods,
                "champion"   : champ,
                "debut"      : debut,
                "academy"    : academy,
                "birth_year" : birth_year,
                "seasons"    : seasons,
                "last_season": last_season,
            }
            self.drivers_data[drv] = teams

        # Índice normalizado para autocomplete
        self.all_drivers = list(self.drivers_meta.keys())

        # Categorías
        self.all_categories = self._build_categories()

        # Cache de pilotos por categoría
        self._cache = {}

    # ── Construir categorías ──────────────────────────────────────
    def _build_categories(self):
        cats = []

        # Equipos
        all_teams = list({t for ts in self.drivers_data.values() for t in ts})
        for t in all_teams:
            cats.append({
                "label": t.upper(),
                "type" : "team",
                "key"  : f"team:{t}",
                "check": lambda d, _t=t: _t in self.drivers_meta[d]["teams"],
            })

        # Nacionalidades con ≥3 pilotos
        nat_count = defaultdict(int)
        for m in self.drivers_meta.values():
            nat_count[m["nationality"]] += 1

        FLAGS = {
            "española":"🇪🇸","británica":"🇬🇧","alemana":"🇩🇪","finlandesa":"🇫🇮",
            "australiana":"🇦🇺","brasileña":"🇧🇷","mexicana":"🇲🇽","francesa":"🇫🇷",
            "monegasca":"🇲🇨","neerlandesa":"🇳🇱","tailandesa":"🇹🇭","argentina":"🇦🇷",
            "canadiense":"🇨🇦","rusa":"🇷🇺","italiana":"🇮🇹","japonesa":"🇯🇵",
            "austriaca":"🇦🇹","colombiana":"🇨🇴","venezolana":"🇻🇪","polaca":"🇵🇱",
            "danesa":"🇩🇰","neozelandesa":"🇳🇿","sueca":"🇸🇪","sudafricana":"🇿🇦",
            "estadounidense":"🇺🇸","suiza":"🇨🇭","india":"🇮🇳","portuguesa":"🇵🇹",
            "húngara":"🇭🇺","belga":"🇧🇪","irlandesa":"🇮🇪","china":"🇨🇳",
            "noruega":"🇳🇴","estonia":"🇪🇪","singapurense":"🇸🇬","turca":"🇹🇷",
            "indonesia":"🇮🇩","checa":"🇨🇿","ecuatoriana":"🇪🇨",
        }
        for nat, cnt in nat_count.items():
            if cnt >= 2:
                flag = FLAGS.get(nat, "🏁")
                cats.append({
                    "label": f"{flag} {nat.capitalize()}",
                    "type" : "nationality",
                    "key"  : f"nat:{nat}",
                    "check": lambda d, _n=nat: self.drivers_meta[d]["nationality"] == _n,
                })

        # Victorias
        for mn, mx, lbl in [(1,999,"≥1 Victoria"),(5,999,"≥5 Victorias"),(10,999,"≥10 Victorias"),(0,0,"0 Victorias")]:
            cats.append({
                "label": lbl, "type": "wins", "key": f"wins:{mn}:{mx}",
                "check": lambda d, mn=mn, mx=mx: mn <= self.drivers_meta[d]["wins"] <= mx,
            })

        # Podios
        for mn, mx, lbl in [(1,999,"≥1 Podio"),(5,999,"≥5 Podios"),(10,999,"≥10 Podios"),(0,0,"0 Podios")]:
            cats.append({
                "label": lbl, "type": "podiums", "key": f"pods:{mn}:{mx}",
                "check": lambda d, mn=mn, mx=mx: mn <= self.drivers_meta[d]["podiums"] <= mx,
            })

        # Campeón
        champ_lbl = self.champion_label
        cats.append({
            "label": f"🏆 {champ_lbl}",
            "type" : "champion", "key": "champ:yes",
            "check": lambda d: bool(self.drivers_meta[d]["champion"]),
        })
        cats.append({
            "label": "❌ Sin título",
            "type" : "champion", "key": "champ:no",
            "check": lambda d: self.drivers_meta[d]["champion"] is False,
        })

        # Número de escuderías
        for n, lbl in [(2,"≥2 Escuderías"),(3,"≥3 Escuderías"),(4,"≥4 Escuderías"),(5,"≥5 Escuderías")]:
            cats.append({
                "label": lbl, "type": "num_teams", "key": f"nteams:{n}",
                "check": lambda d, _n=n: len(set(self.drivers_meta[d]["teams"])) >= _n,
            })
        cats.append({
            "label": "1 Sola Escudería", "type": "num_teams", "key": "nteams:1",
            "check": lambda d: len(set(self.drivers_meta[d]["teams"])) == 1,
        })

        # Época de debut
        debut_brackets = [
            (0,    1969, "Debut antes de 1970 🕰️"),
            (1970, 1979, "Debut años 70 🪩"),
            (1980, 1989, "Debut años 80 🎸"),
            (1990, 1999, "Debut años 90 💿"),
            (2000, 2009, "Debut años 2000 📱"),
            (2010, 2019, "Debut años 2010 📲"),
            (2020, 9999, "Debut años 2020 🚀"),
            (0,    1999, "Debut antes del 2000 📼"),
            (2000, 9999, "Debut en 2000 o después 💻"),
        ]
        for y1, y2, lbl in debut_brackets:
            has = any(
                y1 <= m["debut"] <= y2
                for m in self.drivers_meta.values()
                if m["debut"] > 0
            )
            if has:
                cats.append({
                    "label": lbl, "type": "debut", "key": f"debut:{y1}:{y2}",
                    "check": lambda d, _y1=y1, _y2=y2: _y1 <= self.drivers_meta[d]["debut"] <= _y2,
                })

        # Academias
        academy_defs = [
            ("ferrari",   "🔴 Academia Ferrari"),
            ("red bull",  "🐂 Academia Red Bull"),
            ("mercedes",  "⭐ Academia Mercedes"),
            ("mclaren",   "🟠 Academia McLaren"),
            ("alpine",    "🔵 Academia Alpine/Renault"),
            ("sauber",    "🟢 Academia Sauber/Alfa"),
            ("haas",      "🇺🇸 Academia Haas"),
            ("williams",  "🏴󠁧󠁢󠁥󠁮󠁧󠁿 Academia Williams"),
        ]
        for ac_key, ac_lbl in academy_defs:
            has = any(
                ac_key in (m["academy"] or "")
                for m in self.drivers_meta.values()
            )
            if has:
                cats.append({
                    "label": ac_lbl, "type": "academy", "key": f"academy:{ac_key}",
                    "check": lambda d, _ak=ac_key: _ak in (self.drivers_meta[d]["academy"] or ""),
                })

        # Debut joven (menores de 20 años al debutar)
        young_entries = [
            (d, m["debut"] - m["birth_year"])
            for d, m in self.drivers_meta.items()
            if m["debut"] > 0 and m["birth_year"] > 0
        ]
        for max_age, lbl in [(19, "Debutó con ≤19 años 🧒"), (20, "Debutó con ≤20 años 🧒")]:
            if any(age <= max_age for _, age in young_entries):
                cats.append({
                    "label": lbl, "type": "age_debut", "key": f"age_debut:{max_age}",
                    "check": lambda d, _a=max_age: (
                        self.drivers_meta[d]["debut"] > 0 and
                        self.drivers_meta[d]["birth_year"] > 0 and
                        (self.drivers_meta[d]["debut"] - self.drivers_meta[d]["birth_year"]) <= _a
                    ),
                })

        # Sin puntos / con puntos
        cats.append({
            "label": "Nunca sumó puntos 🔲", "type": "points", "key": "points:zero",
            "check": lambda d: self.drivers_meta[d]["wins"] == 0 and self.drivers_meta[d]["podiums"] == 0,
        })

        # Proveedor de motor (F1 únicamente — se activa solo si el campo existe)
        ENGINE_SUPPLIERS = {
            "mercedes engine": (
                "🔧 Motor Mercedes",
                ["mercedes","mclaren","williams","force india","racing point","brawn gp","aston martin","alpine"],
            ),
            "ferrari engine": (
                "🔧 Motor Ferrari",
                ["ferrari","sauber","alfa romeo","haas","toro rosso","alphatauri","racing bulls",
                 "marussia","manor","caterham"],
            ),
            "renault engine": (
                "🔧 Motor Renault/Alpine",
                ["renault","alpine","red bull","toro rosso","lotus","caterham","virgin","spirit"],
            ),
            "honda engine": (
                "🔧 Motor Honda",
                ["red bull","alphatauri","racing bulls","toro rosso","bar","honda",
                 "super aguri","racing point"],
            ),
        }
        for key, (lbl, teams_with_engine) in ENGINE_SUPPLIERS.items():
            if any(
                any(t in teams_with_engine for t in m["teams"])
                for m in self.drivers_meta.values()
            ):
                cats.append({
                    "label": lbl, "type": "engine", "key": f"engine:{key}",
                    "check": lambda d, _tw=teams_with_engine:
                        any(t in _tw for t in self.drivers_meta[d]["teams"]),
                })

        # Número de temporadas activas
        for n, lbl in [(5,"≥5 Temporadas"),(10,"≥10 Temporadas"),(15,"≥15 Temporadas")]:
            if any(m["seasons"] >= n for m in self.drivers_meta.values()):
                cats.append({
                    "label": lbl, "type": "seasons", "key": f"seasons:{n}",
                    "check": lambda d, _n=n: self.drivers_meta[d]["seasons"] >= _n,
                })
        cats.append({
            "label": "Solo 1 Temporada ☄️", "type": "seasons", "key": "seasons:1",
            "check": lambda d: self.drivers_meta[d]["seasons"] == 1,
        })

        # Compañero de equipo de leyendas — datos reales, no inferidos
        # Solo pilotos que efectivamente compartieron equipo en el mismo año
        REAL_TEAMMATES = {
            "schumacher": (
                "🔴 Compañero de M. Schumacher",
                # Benetton 1991-95, Ferrari 1996-2006, Mercedes 2010-12
                {
                    "johnny herbert","martin brundle","jose luis bugalski",
                    "JJ lehto","jos verstappen","eddie irvine","rubens barrichello",
                    "felipe massa","kimi raikkonen","nico rosberg","michael schumacher",
                    # Benetton compañeros reales:
                    "nelson piquet jr","michael schumacher",
                },
                {"michael schumacher"},
            ),
            "senna": (
                "🟡 Compañero de Senna",
                # Toleman 1984, Lotus 1985-87, McLaren 1988-92, Williams 1994
                {
                    "johnny cecotto","stefan johansson","derek warwick","satoru nakajima",
                    "alain prost","gerhard berger","mika hakkinen","damon hill",
                    "ayrton senna",
                },
                {"ayrton senna"},
            ),
            "hamilton": (
                "⭐ Compañero de Hamilton",
                # McLaren 2007-12, Mercedes 2013-24, Ferrari 2025
                {
                    "fernando alonso","heikki kovalainen","jenson button","nico rosberg",
                    "valtteri bottas","george russell","charles leclerc","lewis hamilton",
                },
                {"lewis hamilton"},
            ),
            "verstappen": (
                "🐂 Compañero de Verstappen",
                # Toro Rosso 2015, Red Bull 2016-present
                {
                    "carlos sainz","daniel ricciardo","pierre gasly","alex albon",
                    "sergio perez","liam lawson","max verstappen","yuki tsunoda",
                },
                {"max verstappen"},
            ),
            "alonso": (
                "🔵 Compañero de Alonso",
                # Minardi 2001, Renault 2003-06, McLaren 2007, Renault 2008-09,
                # Ferrari 2010-14, McLaren 2015-17, Alpine 2021-22, Aston Martin 2023+
                {
                    "tarso marques","jenson button","giancarlo fisichella","jarno trulli",
                    "lewis hamilton","nelson piquet jr","robert kubica","felipe massa",
                    "kimi raikkonen","luca badoer","stoffel vandoorne","esteban ocon",
                    "lance stroll","fernando alonso",
                },
                {"fernando alonso"},
            ),
            "prost": (
                "🏆 Compañero de Prost",
                # Renault 1981-83, McLaren 1984-89, Ferrari 1990-91, Williams 1993
                {
                    "rene arnoux","niki lauda","ayrton senna","gerhard berger",
                    "nigel mansell","damon hill","jean alesi","ivan capelli",
                    "alain prost",
                },
                {"alain prost"},
            ),
            "lauda": (
                "🎯 Compañero de Lauda",
                # March 1972, BRM 1973, Ferrari 1974-77, Brabham 1978-79, McLaren 1982-85
                {
                    "arturo merzario","clay regazzoni","carlos reutemann","gilles villeneuve",
                    "john watson","alain prost","niki lauda",
                },
                {"niki lauda"},
            ),
        }
        for key, (lbl, real_teammates, legend_names) in REAL_TEAMMATES.items():
            if not any(ln in self.drivers_meta for ln in legend_names):
                continue
            valid_teammates = {
                t for t in real_teammates
                if t in self.drivers_meta and t not in legend_names
            }
            if not valid_teammates:
                continue
            cats.append({
                "label": lbl, "type": "teammate", "key": f"teammate:{key}",
                "check": lambda d, _vt=valid_teammates, _ln=legend_names: (
                    d not in _ln and d in _vt
                ),
            })

        # Piloto activo (last_season == 0 significa aún en activo)
        cats.append({
            "label": "Piloto activo 🟢", "type": "active", "key": "active:yes",
            "check": lambda d: self.drivers_meta[d]["last_season"] == 0,
        })
        # Piloto retirado antes de 2000
        if any(0 < m["last_season"] < 2000 for m in self.drivers_meta.values()):
            cats.append({
                "label": "Retirado antes de 2000 📼", "type": "active", "key": "active:pre2000",
                "check": lambda d: 0 < self.drivers_meta[d]["last_season"] < 2000,
            })
        # Corrió en los 2000s (debut o last_season en 2000-2009)
        cats.append({
            "label": "Corrió en los 2000s 📱", "type": "active", "key": "active:2000s",
            "check": lambda d: (
                (self.drivers_meta[d]["debut"] <= 2009 and
                 (self.drivers_meta[d]["last_season"] == 0 or self.drivers_meta[d]["last_season"] >= 2000))
            ),
        })

        return cats

    def get_cats_of_types(self, types, popular_only=False):
        result = []
        for c in self.all_categories:
            if c["type"] not in types:
                continue
            if popular_only and c["type"] == "team":
                base_key = c["key"].split(":", 1)[1]
                if base_key not in self.popular_teams:
                    continue
            # Excluir categorías con menos de 2 pilotos (imposibles o triviales en grid)
            if len(self.cached_drivers(c)) < 2:
                continue
            result.append(c)
        return result

    def cached_drivers(self, cat):
        k = cat["key"]
        if k not in self._cache:
            self._cache[k] = set(d for d in self.drivers_meta if cat["check"](d))
        return self._cache[k]

    def drivers_satisfying(self, cat_a, cat_b):
        return list(self.cached_drivers(cat_a) & self.cached_drivers(cat_b))

    def generate_grid(self, cfg):
        size        = cfg["grid_size"]
        min_sol     = cfg["min_solutions"]
        pop_only    = cfg.get("popular_only", False)
        prefer_rare = cfg.get("prefer_rare", False)

        row_pool = self.get_cats_of_types(cfg["cat_types_row"], pop_only)
        col_pool = self.get_cats_of_types(cfg["cat_types_col"], pop_only)

        # Si el pool es muy chico, ampliar quitando restricciones
        if len(row_pool) < size or len(col_pool) < size:
            row_pool = self.get_cats_of_types(cfg["cat_types_row"], False)
            col_pool = self.get_cats_of_types(cfg["cat_types_col"], False)

        for _ in range(5000):
            if len(row_pool) < size or len(col_pool) < size:
                break
            row_cats = random.sample(row_pool, size)
            col_cats = random.sample(col_pool, size)

            if {c["key"] for c in row_cats} & {c["key"] for c in col_cats}:
                continue

            valid     = True
            total_sol = 0
            for rc in row_cats:
                for cc in col_cats:
                    s = self.drivers_satisfying(rc, cc)
                    n = len(s)
                    if n < min_sol:       # garantía fuerte: NUNCA celda vacía
                        valid = False
                        break
                    total_sol += n
                if not valid:
                    break
            if not valid:
                continue

            if prefer_rare and total_sol / (size * size) > 5:
                continue

            return row_cats, col_cats

        # Fallback: relajar prefer_rare y reducir min_sol (nunca a 0)
        if min_sol > 1 or prefer_rare:
            return self.generate_grid({
                **cfg,
                "min_solutions": max(1, min_sol - 1),
                "popular_only" : False,
                "prefer_rare"  : False,
            })

        # Último recurso: devolver el mejor grid encontrado (min 1 sol garantizada
        # por el filtro de get_cats_of_types que exige ≥2 pilotos por categoría)
        for _ in range(500):
            if len(row_pool) < size or len(col_pool) < size:
                break
            row_cats = random.sample(row_pool, size)
            col_cats = random.sample(col_pool, size)
            if {c["key"] for c in row_cats} & {c["key"] for c in col_cats}:
                continue
            # Verificar que TODAS las celdas tengan al menos 1 solución
            valid = all(
                len(self.drivers_satisfying(rc, cc)) >= 1
                for rc in row_cats for cc in col_cats
            )
            if valid:
                return row_cats, col_cats

        # Si absolutamente nada funciona, devolver el primer grid sin garantía
        # (caso imposible en práctica con las BDs actuales)
        row_cats = random.sample(row_pool, min(size, len(row_pool)))
        col_cats = random.sample(col_pool, min(size, len(col_pool)))
        return row_cats, col_cats


# ══════════════════════════════════════════════════════════════════
#  BASE DE DATOS — FÓRMULA 3 / F3 INTERNACIONAL / GP3
#  (equipos, nacionalidad, victorias_f3, podios_f3, campeón_f3)
# ══════════════════════════════════════════════════════════════════
RAW_F3 = {
    # ── Campeones F3 Internacional / GP3 ─────────────────────────
    "esteban ocon"          : (["prema"],                                                        "francesa",         6, 12, True, 2014, "mercedes", 1996, 1, 2014),     # F3 Europea 2014
    "felix rosenqvist"      : (["prema"],                                                        "sueca",            8, 15, True, 2015, "", 1991, 1, 2015),     # F3 Europea 2015
    "lance stroll"          : (["prema"],                                                        "canadiense",       7, 12, True, 2016, "", 1998, 1, 2016),     # F3 Europea 2016
    "joel eriksson"         : (["motopark"],                                                     "sueca",            5,  9, True, 2017, "", 1998, 1, 2017),     # F3 Europea 2017
    "george russell"        : (["hitech"],                                                       "británica",        7, 14, True, 2017, "mercedes", 1998, 1, 2018),     # GP3 2017 / F3 Int 2018 campeón
    "maximilian gunther"    : (["prema"],                                                        "alemana",          4,  9, False, 2016, "", 1997, 1, 0),
    "callum ilott"          : (["sauber junior","carlin"],                                       "británica",        3,  7, False, 2017, "ferrari", 1998, 2, 2018),
    "juri vips"             : (["hitech"],                                                       "estonia",          2,  5, False, 2019, "red bull", 2000, 1, 2019),
    "christian lundgaard"   : (["art"],                                                          "danesa",           4,  9, False, 2019, "alpine", 2001, 1, 2019),
    "oscar piastri"         : (["prema"],                                                        "australiana",      7, 13, True, 2020, "alpine", 2001, 1, 2020),     # F3 Int 2020
    "logan sargeant"        : (["carlin"],                                                       "estadounidense",   3,  7, False, 2021, "williams", 2000, 2, 2021),
    "dennis hauger"         : (["prema"],                                                        "noruega",          8, 14, True, 2021, "red bull", 2002, 1, 2021),     # F3 Int 2021
    "victor martins"        : (["art"],                                                          "francesa",         5, 10, True, 2022, "alpine", 2002, 2, 2022),     # F3 Int 2022
    "gabriel bortoleto"     : (["trident","prema"],                                              "brasileña",        6, 12, True, 2023, "mclaren", 2004, 1, 2023),   # F3 Int 2023
    "franco colapinto"      : (["van amersfoort","campos"],                                      "argentina",        2,  5, False, 2022, "williams", 2003, 2, 2022),
    "frederic vesti"        : (["sauber junior","prema"],                                        "danesa",           5,  9, False, 2021, "mercedes", 2001, 2, 2022),
    "arthur leclerc"        : (["prema"],                                                        "monegasca",        2,  5, False, 2022, "ferrari", 2000, 2, 2022),
    "roman stanek"          : (["trident","prema"],                                              "checa",            2,  4, False, 2022, "", 2002, 2, 2023),
    "ayumu iwasa"           : (["hitech"],                                                       "japonesa",         2,  5, False, 2022, "red bull", 2002, 2, 2022),
    "jake hughes"           : (["hitech"],                                                       "británica",        3,  6, False, 2020, "mercedes", 1994, 2, 2020),
    "juan manuel correa"    : (["art","sauber junior"],                                          "estadounidense",   1,  3, False, 2019, "ferrari", 1999, 2, 2019),
    "david schumacher"      : (["charouz","trident"],                                            "alemana",          1,  3, False, 2021, "haas", 1999, 2, 0),
    "clement novalak"       : (["trident","campos"],                                             "francesa",         1,  2, False, 2021, "", 1999, 2, 2021),
    "enzo fittipaldi"       : (["charouz"],                                                      "brasileña",        1,  2, False, 2019, "haas", 2000, 2, 0),
    "calan williams"        : (["campos","trident","prema"],                                     "australiana",      0,  1, False, 2021, "", 2000, 2, 2021),
    "caio collet"           : (["mp motorsport"],                                                "brasileña",        2,  5, False, 2022, "alpine", 2001, 2, 0),
    "kaylen frederick"      : (["carlin"],                                                       "estadounidense",   0,  1, False, 2022, "", 2000, 1, 0),
    "alex smolarz"          : (["hitech","jenzer"],                                              "alemana",          0,  0, False, 2022, "", 2001, 1, 0),
    "pierre-louis chovet"   : (["campos"],                                                       "francesa",         1,  2, False, 2021, "", 2001, 1, 0),
    "amaury cordeel"        : (["campos","van amersfoort"],                                      "belga",            0,  0, False, 2022, "", 2000, 2, 2022),
    "sebastien ogier"       : (["carlin"],                                                       "francesa",         0,  0, False, 2022, "", 2001, 1, 0),
    "liam lawson"           : (["hitech","carlin"],                                              "neozelandesa",     3,  7, False, 2020, "red bull", 2002, 2, 2021),
    "jack doohan"           : (["trident","art"],                                                "australiana",      2,  5, False, 2022, "alpine", 2003, 1, 0),
    "theo pourchaire"       : (["art","sauber junior"],                                          "francesa",         4,  8, False, 2021, "sauber", 2003, 1, 0),
    "robert shwartzman"     : (["prema"],                                                        "rusa",             6, 11, True, 2019, "ferrari", 1999, 1, 0),     # F3 Int 2019
    "marcus armstrong"      : (["prema","art"],                                                  "neozelandesa",     2,  5, False, 2019, "ferrari", 2000, 2, 2021),
    "yuki tsunoda"          : (["jenzer","carlin"],                                              "japonesa",         2,  5, False, 2019, "red bull", 2000, 1, 2020),
    "jake dennis"           : (["carlin"],                                                       "británica",        0,  1, False, 2018, "red bull", 1995, 1, 0),
    "alex palou"            : (["campos"],                                                       "española",         0,  1, False, 2018, "", 1997, 1, 0),
    "giuliano alesi"        : (["trident"],                                                      "francesa",         0,  1, False, 2019, "ferrari", 1999, 1, 0),
    "tatiana calderon"      : (["jenzer","charouz"],                                             "colombiana",       0,  0, False, 2018, "sauber", 1993, 1, 0),
    "giulio moises"         : (["campos"],                                                       "ecuatoriana",      0,  0, False, 2021, "", 1998, 1, 0),
    "sara bovy"             : (["jenzer"],                                                       "belga",            0,  0, False, 2022, "", 1992, 1, 0),
    "niko kari"             : (["trident","mp motorsport"],                                      "finlandesa",       1,  3, False, 2017, "", 1998, 1, 0),
    "ryan tveter"           : (["trident"],                                                      "estadounidense",   0,  0, False, 0, "", 1992, 1, 0),
    "joey mawson"           : (["van amersfoort"],                                               "australiana",      1,  4, False, 2016, "", 1997, 1, 0),
    "guanyu zhou"           : (["art","virtuosi"],                                               "china",            3,  7, False, 2019, "alpine", 1999, 1, 2019),
    "jann mardenborough"    : (["carlin"],                                                       "británica",        0,  1, False, 2015, "", 1991, 1, 0),
    "antonio fuoco"         : (["prema","carlin"],                                               "italiana",         2,  5, False, 2015, "ferrari", 1996, 1, 0),
    "arjun maini"           : (["jenzer","trident"],                                             "india",            0,  1, False, 2016, "", 1995, 1, 0),
    "sergio sette camara"   : (["carlin","motopark"],                                            "brasileña",        2,  4, False, 2016, "red bull", 1996, 1, 0),
    "dan ticktum"           : (["carlin","dams"],                                                "británica",        2,  5, False, 2018, "red bull", 1999, 1, 2019),
    "nikita mazepin"        : (["art"],                                                          "rusa",             1,  2, False, 2018, "", 1999, 1, 0),
    "mick schumacher"       : (["prema"],                                                        "alemana",          4,  8, False, 2018, "ferrari", 1999, 1, 0),
    "max fewtrell"          : (["art"],                                                          "británica",        2,  4, False, 2018, "", 1998, 1, 0),
    "lirim zendeli"         : (["trident","sms"],                                                "alemana",          2,  4, False, 2019, "", 1997, 1, 0),
    "bent viscaal"          : (["trident"],                                                      "neerlandesa",      1,  2, False, 2020, "", 1999, 1, 0),
    "lukas dunner"          : (["charouz","van amersfoort"],                                     "austriaca",        0,  1, False, 2020, "", 2000, 1, 0),
    "matteo nannini"        : (["campos"],                                                       "italiana",         0,  1, False, 2021, "red bull", 2003, 1, 0),
    "kush maini"            : (["campos","mp motorsport"],                                       "india",            1,  3, False, 2021, "", 1999, 2, 2022),
    "nazim lapierre"        : (["jenzer"],                                                       "francesa",         0,  0, False, 2022, "", 2001, 1, 0),
    "hamda al qubaisi"      : (["prema"],                                                        "emiratí",          0,  0, False, 2023, "", 2002, 1, 0),
    "mari boya"             : (["campos"],                                                       "española",         0,  0, False, 2024, "", 2003, 1, 0),
    "sebastian priaulx"     : (["carlin"],                                                       "británica",        0,  1, False, 2023, "", 2000, 1, 0),
    "browning"              : (["jenzer"],                                                       "británica",        0,  0, False, 2023, "", 2002, 1, 0),
    "bence valint"          : (["campos"],                                                       "húngara",          0,  0, False, 2024, "", 2004, 1, 0),
    "sebastien buemi"       : (["carlin"],                                                       "suiza",            0,  1, False, 2006, "red bull", 1988, 1, 0),
    # ── Pilotos F3 adicionales ────────────────────────────────────
    "sophia floersch"       : (["van amersfoort","campos"],                                                      "alemana",           0,   0, False, 2019, "", 1997, 1, 0),
    "pedro piquet"          : (["trident"],                                                                      "brasileña",         0,   0, False, 2019, "", 2000, 1, 0),
    "marino sato"           : (["trident","dams"],                                                               "japonesa",          0,   0, False, 2021, "", 1997, 2, 2022),
    "sebastian ogier"       : (["carlin"],                                                                       "francesa",          0,   0, False, 0, "", 2001, 1, 0),
    "david beckmann"        : (["charouz","campos"],                                                              "alemana",           0,   0, False, 2019, "", 2000, 1, 2020),

    # ── F3 adicionales ───────────────────────────────────────────
    "andrea kimi antonelli" : (["prema"],                                                                         "italiana",          6,  13, True,  2023, "mercedes", 2006, 1, 2023),
    "oliver bearman"        : (["prema"],                                                                         "británica",         3,   7, False, 2022, "ferrari",  2005, 1, 2022),
    "isack hadjar"          : (["hitech"],                                                                         "francesa",          2,   5, False, 2023, "red bull", 2004, 1, 2023),
    "zak o'sullivan"        : (["prema"],                                                                         "británica",         4,   8, True,  2022, "mercedes", 2003, 1, 2022),
    "paul aron"             : (["prema","hitech"],                                                                "estonia",           2,   5, False, 2022, "ferrari",  2003, 2, 2023),
    "pepe marti"            : (["prema"],                                                                         "española",          1,   3, False, 2023, "ferrari",  2004, 1, 2023),
    "oliver goethe"         : (["trident"],                                                                       "alemana",           1,   2, False, 2023, "",         2003, 1, 2023),
    "dino beganovic"        : (["prema"],                                                                         "sueca",             2,   5, False, 2022, "ferrari",  2003, 1, 2022),
    "jak crawford"          : (["hitech"],                                                                        "estadounidense",    2,   4, False, 2022, "red bull", 2003, 1, 2022),
    "nikola tsolov"         : (["art"],                                                                           "búlgara",           2,   4, False, 2024, "",         2006, 1, 2024),
    "alex dunne"            : (["mp motorsport"],                                                                  "irlandesa",         3,   6, False, 2024, "mclaren",  2005, 1, 2024),
    "ralf aron"             : (["hitech","prema"],                                                                "estonia",           2,   5, False, 2022, "ferrari",  2003, 2, 2023),
    "leonardo fornaroli"    : (["trident"],                                                                       "italiana",          1,   3, False, 2024, "ferrari",  2005, 1, 2024),
    "tim tramnitz"          : (["mp motorsport"],                                                                  "alemana",           2,   4, False, 2023, "",         2003, 1, 2023),
    "reece ushijima"        : (["van amersfoort"],                                                                "japonesa",          0,   1, False, 2023, "",         2003, 1, 2023),
    "ryan lim"              : (["rodin"],                                                                         "singapurense",      0,   0, False, 2024, "",         2004, 1, 2024),
    "sami meguetounif"      : (["prema"],                                                                         "francesa",          1,   3, False, 2024, "",         2005, 1, 2024),
    # ── F3 2025 ──────────────────────────────────────────────────
    "tuukka taponen"        : (["prema"],                                                                         "finlandesa",        3,   6, False, 2024, "red bull", 2005, 1, 0),
    "christian mansell"     : (["carlin","campos"],                                                               "australiana",       1,   3, False, 2023, "",         2002, 2, 0),
    "arvid lindblad"        : (["hitech","prema"],                                                                "británica",         4,   8, False, 2024, "red bull", 2006, 1, 0),
    "charlie wurz"          : (["trident"],                                                                       "austriaca",         0,   2, False, 2024, "",         2005, 1, 0),
    "james wharton"         : (["prema"],                                                                         "australiana",       1,   3, False, 2024, "red bull", 2005, 1, 0),
    "gabriel bueno"         : (["art"],                                                                           "brasileña",         0,   1, False, 2024, "",         2006, 1, 0),
    "aiden james"           : (["van amersfoort"],                                                                "neozelandesa",      0,   0, False, 2025, "",         2005, 1, 0),
    "kirill smal"           : (["prema"],                                                                         "georgiana",         0,   1, False, 2025, "",         2006, 1, 0),
}

# ══════════════════════════════════════════════════════════════════
#  INSTANCIAR LAS TRES SERIES
# ══════════════════════════════════════════════════════════════════
F1_POPULAR_TEAMS = [
    "ferrari","mercedes","red bull","mclaren","renault","williams",
    "lotus","sauber","force india","haas","alphatauri","toro rosso",
    "benetton","jordan","aston martin","alfa romeo","alpine","racing point",
    "brawn gp","bmw sauber","toyota","cooper","brabham","tyrrell","brm",
]
F2_POPULAR_TEAMS = [
    "prema","art","dams","carlin","hitech","virtuosi","mp motorsport",
    "campos","trident","charouz","arden","russian time","isport",
    "rapax","racing engineering","uni-virtuosi","invicta",
]

F3_POPULAR_TEAMS = [
    "prema","art","hitech","carlin","trident","campos","charouz",
    "sauber junior","van amersfoort","mp motorsport","dams","motopark","jenzer",
]

# ── Joshua Duerksen ──────────────────────────────────────────────
# ── Joshua Dürksen — datos corregidos ────────────────────────────
# Nunca corrió en F3 Internacional. Trayectoria: F4 UAE/Italia/ADAC → FRECA (2022-23) → F2 (2024-26)
# F2: 2024 AIX Racing (2 victorias, 4 podios, 10º camp.) | 2025 AIX Racing (2 victorias, 8 podios, 9º camp.)
# 2026 Invicta Racing + Piloto de desarrollo Mercedes
# Total F2 hasta fin 2025: 4 victorias, 12 podios
RAW_F2["joshua duerksen"] = (["aix racing","invicta"], "paraguaya", 4, 12, False, 2024, "mercedes", 2002, 2, 0)

FLAGS_GLOBAL = {
    "española":"🇪🇸","británica":"🇬🇧","alemana":"🇩🇪","finlandesa":"🇫🇮",
    "australiana":"🇦🇺","brasileña":"🇧🇷","mexicana":"🇲🇽","francesa":"🇫🇷",
    "monegasca":"🇲🇨","neerlandesa":"🇳🇱","tailandesa":"🇹🇭","argentina":"🇦🇷",
    "canadiense":"🇨🇦","rusa":"🇷🇺","italiana":"🇮🇹","japonesa":"🇯🇵",
    "austriaca":"🇦🇹","colombiana":"🇨🇴","venezolana":"🇻🇪","polaca":"🇵🇱",
    "danesa":"🇩🇰","neozelandesa":"🇳🇿","sueca":"🇸🇪","sudafricana":"🇿🇦",
    "estadounidense":"🇺🇸","suiza":"🇨🇭","india":"🇮🇳","portuguesa":"🇵🇹",
    "húngara":"🇭🇺","belga":"🇧🇪","irlandesa":"🇮🇪","china":"🇨🇳",
    "noruega":"🇳🇴","estonia":"🇪🇪","singapurense":"🇸🇬","turca":"🇹🇷",
    "indonesia":"🇮🇩","checa":"🇨🇿","ecuatoriana":"🇪🇨","paraguaya":"🇵🇾",
    "emiratí":"🇦🇪","búlgara":"🇧🇬",
}

# ══════════════════════════════════════════════════════════════════
#  CLASE MODO MIXTO — cruza datos de F1, F2 y F3
# ══════════════════════════════════════════════════════════════════
class MixedSeries:
    """
    Combina los tres RAW en un único espacio de pilotos.
    Cada piloto tiene meta_f1, meta_f2, meta_f3 (None si no corrió en esa serie).
    Las categorías son etiquetadas con la serie de origen: "FERRARI (F1)",
    "PREMA (F2)", "Academia Red Bull (F3)", "Campeón F3", etc.
    La verificación requiere que el piloto cumpla AMBAS categorías de su celda
    consultando el dict correcto según el sufijo de serie.
    """
    name           = "🔀 Modo Mixto"
    champion_label = "Campeón en alguna serie"

    def __init__(self):
        # Unir todos los pilotos de los tres RAW
        self.drivers_meta = {}   # name → {f1, f2, f3}  (cada uno es dict o None)
        self.all_drivers  = []

        def build_meta(raw):
            result = {}
            for drv, (teams, nat, wins, pods, champ, debut, academy, birth_year, seasons, last_season) in raw.items():
                result[drv] = {
                    "teams": teams, "nationality": nat,
                    "wins": wins,   "podiums": pods,
                    "champion": champ, "debut": debut,
                    "academy": academy, "birth_year": birth_year,
                    "seasons": seasons,
                    "last_season": last_season,
                }
            return result

        meta_f1 = build_meta(RAW_F1)
        meta_f2 = build_meta(RAW_F2)
        meta_f3 = build_meta(RAW_F3)

        all_names = set(meta_f1) | set(meta_f2) | set(meta_f3)
        for name in all_names:
            self.drivers_meta[name] = {
                "f1": meta_f1.get(name),
                "f2": meta_f2.get(name),
                "f3": meta_f3.get(name),
            }
            # nationality comes from whichever series we have data for
            for src in ("f1","f2","f3"):
                if self.drivers_meta[name][src]:
                    self.drivers_meta[name]["nationality"] = \
                        self.drivers_meta[name][src]["nationality"]
                    break

        self.all_drivers = list(self.drivers_meta.keys())
        self.all_categories = self._build_categories()
        self._cache = {}

    # ── helpers ──────────────────────────────────────────────────
    def _has(self, driver, serie, check_fn):
        """True if driver raced in `serie` and passes check_fn on that serie's meta."""
        m = self.drivers_meta[driver][serie]
        return m is not None and check_fn(m)

    def _build_categories(self):
        cats = []

        # ── Equipos por serie ─────────────────────────────────────
        series_raw = {"f1": (RAW_F1, "F1"), "f2": (RAW_F2, "F2"), "f3": (RAW_F3, "F3")}
        seen_team_keys = set()
        for serie_key, (raw, lbl) in series_raw.items():
            teams = list({t for (ts,*_) in raw.values() for t in ts})
            for t in teams:
                key = f"team:{serie_key}:{t}"
                if key in seen_team_keys: continue
                seen_team_keys.add(key)
                cats.append({
                    "label": f"{t.upper()} ({lbl})",
                    "type" : "team",
                    "key"  : key,
                    "serie": serie_key,
                    "check": lambda d, _s=serie_key, _t=t:
                        self._has(d, _s, lambda m: _t in m["teams"]),
                })

        # ── Nacionalidades con ≥2 pilotos en la base mixta ────────
        nat_count = defaultdict(int)
        for m in self.drivers_meta.values():
            nat_count[m["nationality"]] += 1
        for nat, cnt in nat_count.items():
            if cnt >= 2:
                flag = FLAGS_GLOBAL.get(nat, "🏁")
                cats.append({
                    "label": f"{flag} {nat.capitalize()}",
                    "type" : "nationality",
                    "key"  : f"nat:{nat}",
                    "serie": "any",
                    "check": lambda d, _n=nat: self.drivers_meta[d]["nationality"] == _n,
                })

        # ── Victorias / podios en cada serie ─────────────────────
        for serie_key, serie_lbl in [("f1","F1"),("f2","F2"),("f3","F3")]:
            for mn, lbl in [(1,"≥1 Victoria"),(5,"≥5 Victorias"),(10,"≥10 Victorias")]:
                cats.append({
                    "label": f"{lbl} en {serie_lbl}",
                    "type" : "wins",
                    "key"  : f"wins:{serie_key}:{mn}",
                    "serie": serie_key,
                    "check": lambda d, _s=serie_key, _mn=mn:
                        self._has(d, _s, lambda m: m["wins"] >= _mn),
                })
            for mn, lbl in [(1,"≥1 Podio"),(5,"≥5 Podios"),(10,"≥10 Podios")]:
                cats.append({
                    "label": f"{lbl} en {serie_lbl}",
                    "type" : "podiums",
                    "key"  : f"pods:{serie_key}:{mn}",
                    "serie": serie_key,
                    "check": lambda d, _s=serie_key, _mn=mn:
                        self._has(d, _s, lambda m: m["podiums"] >= _mn),
                })

        # ── Campeones por serie ───────────────────────────────────
        for serie_key, serie_lbl, champ_lbl in [
            ("f1","F1","Campeón F1 🏆"),
            ("f2","F2","Campeón F2/GP2 🏆"),
            ("f3","F3","Campeón F3 🏆"),
        ]:
            cats.append({
                "label": champ_lbl,
                "type" : "champion",
                "key"  : f"champ:{serie_key}",
                "serie": serie_key,
                "check": lambda d, _s=serie_key:
                    self._has(d, _s, lambda m: bool(m["champion"])),
            })

        # ── Corrió en múltiples series ────────────────────────────
        for series_combo, key, lbl in [
            (["f1","f2"], "in_f1_f2", "Corrió en F1 y F2 🔀"),
            (["f1","f3"], "in_f1_f3", "Corrió en F1 y F3 🔀"),
            (["f2","f3"], "in_f2_f3", "Corrió en F2 y F3 🔀"),
            (["f1","f2","f3"], "in_all", "Corrió en F1+F2+F3 🎖️"),
        ]:
            cats.append({
                "label": lbl,
                "type" : "multiseries",
                "key"  : key,
                "serie": "any",
                "check": lambda d, _sc=series_combo:
                    all(self.drivers_meta[d][s] is not None for s in _sc),
            })

        # ── Número de escuderías — por serie y en total ───────────
        # Por serie individual
        for serie_key, serie_lbl in [("f1","F1"), ("f2","F2"), ("f3","F3")]:
            for n, lbl in [(2,"≥2 Escuderías"),(3,"≥3 Escuderías"),(4,"≥4 Escuderías"),(5,"≥5 Escuderías")]:
                cats.append({
                    "label": f"{lbl} en {serie_lbl}",
                    "type" : "num_teams",
                    "key"  : f"nteams:{serie_key}:{n}",
                    "serie": serie_key,
                    "check": lambda d, _s=serie_key, _n=n:
                        self.drivers_meta[d][_s] is not None and
                        len(set(self.drivers_meta[d][_s]["teams"])) >= _n,
                })
            cats.append({
                "label": f"1 Sola Escudería en {serie_lbl}",
                "type" : "num_teams",
                "key"  : f"nteams:{serie_key}:1",
                "serie": serie_key,
                "check": lambda d, _s=serie_key:
                    self.drivers_meta[d][_s] is not None and
                    len(set(self.drivers_meta[d][_s]["teams"])) == 1,
            })

        # Entre todas las series combinadas
        for n, lbl in [(4,"≥4 Escuderías"),(5,"≥5 Escuderías"),(6,"≥6 Escuderías"),(7,"≥7 Escuderías")]:
            cats.append({
                "label": f"{lbl} en total (F1+F2+F3)",
                "type" : "num_teams",
                "key"  : f"nteams_any:{n}",
                "serie": "any",
                "check": lambda d, _n=n: len({
                    t
                    for s in ("f1","f2","f3")
                    if self.drivers_meta[d][s]
                    for t in self.drivers_meta[d][s]["teams"]
                }) >= _n,
            })

        # ── Academia ──────────────────────────────────────────────
        academy_defs = [
            ("ferrari",  "🔴 Academia Ferrari"),
            ("red bull", "🐂 Academia Red Bull"),
            ("mercedes", "⭐ Academia Mercedes"),
            ("mclaren",  "🟠 Academia McLaren"),
            ("alpine",   "🔵 Academia Alpine"),
        ]
        for ac_key, ac_lbl in academy_defs:
            cats.append({
                "label": ac_lbl,
                "type" : "academy",
                "key"  : f"acad:{ac_key}",
                "serie": "any",
                "check": lambda d, _ak=ac_key: any(
                    self.drivers_meta[d][s] is not None and
                    _ak in (self.drivers_meta[d][s]["academy"] or "")
                    for s in ("f1","f2","f3")
                ),
            })

        # ── Época de debut (en cualquier serie) ───────────────────
        for y1, y2, lbl in [
            (0,    1999, "Debut antes del 2000 📼"),
            (2000, 2009, "Debut años 2000 📱"),
            (2010, 2019, "Debut años 2010 📲"),
            (2020, 9999, "Debut años 2020 🚀"),
        ]:
            cats.append({
                "label": lbl,
                "type" : "debut",
                "key"  : f"debut:{y1}:{y2}",
                "serie": "any",
                "check": lambda d, _y1=y1, _y2=y2: any(
                    self.drivers_meta[d][s] is not None and
                    _y1 <= self.drivers_meta[d][s]["debut"] <= _y2
                    for s in ("f1","f2","f3")
                    if self.drivers_meta[d][s]
                ),
            })

        # ── Debut joven en cualquier serie ────────────────────────
        for max_age, lbl in [(19,"Debutó con ≤19 años 🧒"),(20,"Debutó con ≤20 años 🧒")]:
            cats.append({
                "label": lbl, "type": "age_debut", "key": f"age_debut:{max_age}",
                "serie": "any",
                "check": lambda d, _a=max_age: any(
                    self.drivers_meta[d][s] is not None and
                    self.drivers_meta[d][s]["birth_year"] > 0 and
                    (self.drivers_meta[d][s]["debut"] - self.drivers_meta[d][s]["birth_year"]) <= _a
                    for s in ("f1","f2","f3")
                    if self.drivers_meta[d][s]
                ),
            })

        # ── Sin puntos en F1 ─────────────────────────────────────
        cats.append({
            "label": "Nunca sumó puntos en F1 🔲", "type": "points",
            "key": "points_f1:zero", "serie": "f1",
            "check": lambda d: (
                self.drivers_meta[d]["f1"] is not None and
                self.drivers_meta[d]["f1"]["wins"] == 0 and
                self.drivers_meta[d]["f1"]["podiums"] == 0
            ),
        })

        # ── Temporadas totales en F1 ──────────────────────────────
        for n, lbl in [(5,"≥5 Temporadas en F1"),(10,"≥10 Temporadas en F1"),(15,"≥15 Temporadas en F1")]:
            cats.append({
                "label": lbl, "type": "seasons", "key": f"seasons_f1:{n}", "serie": "f1",
                "check": lambda d, _n=n: (
                    self.drivers_meta[d]["f1"] is not None and
                    self.drivers_meta[d]["f1"]["seasons"] >= _n
                ),
            })

        # ── Motor en F1 ───────────────────────────────────────────
        ENGINE_MAP = {
            "mercedes engine": (
                "🔧 Motor Mercedes (F1)",
                ["mercedes","mclaren","williams","force india","racing point","brawn gp","aston martin"],
            ),
            "ferrari engine": (
                "🔧 Motor Ferrari (F1)",
                ["ferrari","sauber","alfa romeo","haas","toro rosso","alphatauri","racing bulls",
                 "marussia","manor","caterham"],
            ),
        }
        for key, (lbl, teams_with_engine) in ENGINE_MAP.items():
            cats.append({
                "label": lbl, "type": "engine", "key": f"engine_mixed:{key}",
                "serie": "f1",
                "check": lambda d, _tw=teams_with_engine: (
                    self.drivers_meta[d]["f1"] is not None and
                    any(t in _tw for t in self.drivers_meta[d]["f1"]["teams"])
                ),
            })

        # ── Compañero de leyenda (F1) — datos reales ─────────────
        REAL_TM_MIXED = {
            "schumacher": ("🔴 Compañero de M. Schumacher", "michael schumacher", {
                "johnny herbert","martin brundle","jj lehto","jos verstappen",
                "eddie irvine","rubens barrichello","felipe massa","kimi raikkonen",
                "nico rosberg",
            }),
            "senna": ("🟡 Compañero de Senna", "ayrton senna", {
                "johnny cecotto","stefan johansson","derek warwick","satoru nakajima",
                "alain prost","gerhard berger","mika hakkinen","damon hill",
            }),
            "hamilton": ("⭐ Compañero de Hamilton", "lewis hamilton", {
                "fernando alonso","heikki kovalainen","jenson button","nico rosberg",
                "valtteri bottas","george russell","charles leclerc",
            }),
            "verstappen": ("🐂 Compañero de Verstappen", "max verstappen", {
                "carlos sainz","daniel ricciardo","pierre gasly","alex albon",
                "sergio perez","liam lawson","yuki tsunoda",
            }),
        }
        for key, (lbl, legend_name, real_teammates) in REAL_TM_MIXED.items():
            if legend_name not in self.drivers_meta:
                continue
            valid = {t for t in real_teammates if t in self.drivers_meta}
            if not valid:
                continue
            cats.append({
                "label": lbl, "type": "teammate", "key": f"teammate_mixed:{key}",
                "serie": "f1",
                "check": lambda d, _vt=valid, _ln=legend_name: (
                    d != _ln and d in _vt
                ),
            })

        # Piloto activo en cualquier serie
        cats.append({
            "label": "Piloto activo 🟢", "type": "active", "key": "active_mixed:yes",
            "serie": "any",
            "check": lambda d: any(
                self.drivers_meta[d][s] is not None and
                self.drivers_meta[d][s]["last_season"] == 0
                for s in ("f1","f2","f3")
            ),
        })
        # Activo en F1
        cats.append({
            "label": "Activo en F1 🟢", "type": "active", "key": "active_mixed:f1",
            "serie": "f1",
            "check": lambda d: (
                self.drivers_meta[d]["f1"] is not None and
                self.drivers_meta[d]["f1"]["last_season"] == 0
            ),
        })

        return cats

    # ── Pool / cache / generate (same interface as Series) ────────
    def get_cats_of_types(self, types, popular_only=False):
        result = []
        for c in self.all_categories:
            if c["type"] not in types:
                continue
            if len(self.cached_drivers(c)) < 2:
                continue
            result.append(c)
        return result

    def cached_drivers(self, cat):
        k = cat["key"]
        if k not in self._cache:
            self._cache[k] = set(d for d in self.drivers_meta if cat["check"](d))
        return self._cache[k]

    def drivers_satisfying(self, cat_a, cat_b):
        return list(self.cached_drivers(cat_a) & self.cached_drivers(cat_b))

    def generate_grid(self, cfg):
        size        = cfg["grid_size"]
        min_sol     = cfg.get("min_solutions", 1)
        prefer_rare = cfg.get("prefer_rare", False)

        # Categorías disponibles con suficientes pilotos
        row_types = ["team","multiseries","champion","wins","academy","teammate","seasons","age_debut"]
        col_types = ["team","nationality","multiseries","champion","podiums","debut","num_teams","points","engine","seasons","teammate"]

        row_pool = self.get_cats_of_types(row_types)
        col_pool = self.get_cats_of_types(col_types)

        def serie_of(cat):
            """Extrae la serie de una categoría (f1/f2/f3/any)."""
            k = cat["key"]
            for s in ("f1","f2","f3"):
                if f":{s}:" in k or k.endswith(f":{s}"):
                    return s
            return "any"

        def grid_is_balanced(row_cats, col_cats):
            """Verifica que cada celda tenga al menos min_sol soluciones."""
            total = 0
            for rc in row_cats:
                for cc in col_cats:
                    s = self.drivers_satisfying(rc, cc)
                    if len(s) < min_sol:
                        return False, 0
                    total += len(s)
            return True, total

        # Estrategia: preferir que filas y columnas tengan al menos 1 categoría
        # "multiseries" o "any" para garantizar intersección entre series
        for attempt in range(5000):
            if len(row_pool) < size or len(col_pool) < size:
                break
            row_cats = random.sample(row_pool, size)
            col_cats = random.sample(col_pool, size)

            if {c["key"] for c in row_cats} & {c["key"] for c in col_cats}:
                continue

            # Equilibrio: evitar que todas las filas sean de una sola serie
            # y todas las columnas de otra (intersección casi vacía)
            row_series = [serie_of(c) for c in row_cats]
            col_series = [serie_of(c) for c in col_cats]

            row_specific = [s for s in row_series if s != "any"]
            col_specific = [s for s in col_series if s != "any"]
            if (row_specific and col_specific and
                    set(row_specific).isdisjoint(set(col_specific)) and
                    attempt < 2000):
                continue

            # Garantía fuerte: NINGUNA celda puede tener 0 soluciones
            valid, total_sol = grid_is_balanced(row_cats, col_cats)
            if not valid:
                continue

            if prefer_rare and total_sol / (size * size) > 5:
                continue

            return row_cats, col_cats

        # Fallback progresivo: relajar restricciones pero NUNCA permitir celda vacía
        if min_sol > 1 or prefer_rare:
            return self.generate_grid({**cfg, "min_solutions": max(1, min_sol - 1), "prefer_rare": False})

        # Último recurso con garantía de al menos 1 solución por celda
        for _ in range(500):
            if len(row_pool) < size or len(col_pool) < size:
                break
            row_cats = random.sample(row_pool, size)
            col_cats = random.sample(col_pool, size)
            if {c["key"] for c in row_cats} & {c["key"] for c in col_cats}:
                continue
            if all(len(self.drivers_satisfying(rc, cc)) >= 1
                   for rc in row_cats for cc in col_cats):
                return row_cats, col_cats

        row_cats = random.sample(row_pool, min(size, len(row_pool)))
        col_cats = random.sample(col_pool, min(size, len(col_pool)))
        return row_cats, col_cats


SERIES_F1 = Series("🏎️ Fórmula 1", RAW_F1, "Campeón del Mundo",  F1_POPULAR_TEAMS)
SERIES_F2 = Series("🚀 Fórmula 2", RAW_F2, "Campeón de F2/GP2", F2_POPULAR_TEAMS)
SERIES_F3 = Series("🔵 Fórmula 3", RAW_F3, "Campeón de F3",     F3_POPULAR_TEAMS)
SERIES_MIXED = MixedSeries()

SERIES_MAP = {
    "🏎️ Fórmula 1": SERIES_F1,
    "🚀 Fórmula 2": SERIES_F2,
    "🔵 Fórmula 3": SERIES_F3,
    "🔀 Modo Mixto": SERIES_MIXED,
}

# ══════════════════════════════════════════════════════════════════
#  CONFIGURACIÓN DE DIFICULTAD (compartida)
# ══════════════════════════════════════════════════════════════════
DIFFICULTY_CONFIG = {
    "🟢 Fácil": {
        "grid_size"    : 3,
        "time_limit"   : None,
        "allow_repeat" : True,
        "autocomplete" : True,
        "min_solutions": 3,
        "description"  : "Sin tiempo · Repetición permitida · Equipos populares",
        "cat_types_row": ["team"],
        "cat_types_col": ["team","nationality"],
        "popular_only" : True,
    },
    "🟡 Medio": {
        "grid_size"    : 3,
        "time_limit"   : 180,
        "allow_repeat" : False,
        "autocomplete" : False,
        "min_solutions": 2,
        "description"  : "3 minutos · Sin repetir · Equipos + victorias + podios",
        "cat_types_row": ["team","nationality"],
        "cat_types_col": ["team","wins","podiums"],
        "popular_only" : False,
    },
    "🔴 Difícil": {
        "grid_size"    : 4,
        "time_limit"   : 120,
        "allow_repeat" : False,
        "autocomplete" : False,
        "min_solutions": 1,
        "description"  : "2 minutos · Grid 4×4 · Incluye escuderías, épocas y academias",
        "cat_types_row": ["team","nationality","wins","num_teams","debut","age_debut","seasons","teammate","active"],
        "cat_types_col": ["team","podiums","champion","nationality","academy","num_teams","points","engine","seasons","active"],
        "popular_only" : False,
    },
    "💀 Experto": {
        "grid_size"    : 4,
        "time_limit"   : 90,
        "allow_repeat" : False,
        "autocomplete" : False,
        "min_solutions": 1,
        "description"  : "90 segundos · Grid 4×4 · Categorías creativas + intersecciones difíciles",
        "cat_types_row": ["team","wins","champion","num_teams","debut","academy","age_debut","engine","teammate","seasons","active"],
        "cat_types_col": ["nationality","podiums","champion","team","debut","academy","num_teams","points","engine","seasons","teammate","active"],
        "popular_only" : False,
        "prefer_rare"  : True,
    },
}

# ══════════════════════════════════════════════════════════════════
#  HELPERS
# ══════════════════════════════════════════════════════════════════
def normalize(s):
    s = s.lower().strip()
    s = unicodedata.normalize('NFD', s).encode('ascii', 'ignore').decode("utf-8")
    return s

# ══════════════════════════════════════════════════════════════════
#  CLASE PRINCIPAL DEL JUEGO
# ══════════════════════════════════════════════════════════════════

GP_RESULTS = {
    # ── Años 50 ───────────────────────────────────────────────────
     1950: {
        "Gran Premio de Gran Bretaña": ["giuseppe farina","luigi fagioli","reg parnell","yves giraud cabantous","louis rosier","bob gerard","cuth harrison","philippe etancelin","peter walker","joe kelly"],
        "Gran Premio de Mónaco": ["juan manuel fangio","alberto ascari","louis chiron","luigi villoresi","raymond sommer","philippe etancelin","peter whitehead","peter walker","bob gerard","louis rosier"],
        "Gran Premio de Indianápolis": ["johnnie parsons","bill holland","mauri rose","troy ruttman","duane carter","paul russo","jim rathmann","eddie sack","bill cantrell","johnny mantz"],
        "Gran Premio de Suiza": ["giuseppe farina","juan manuel fangio","luigi fagioli","peter whitehead","reg parnell","philippe etancelin","yves giraud cabantous","louis rosier","peter walker","louis chiron"],
        "Gran Premio de Bélgica": ["juan manuel fangio","luigi fagioli","louis rosier","alberto ascari","reg parnell","philippe etancelin","peter whitehead","louis chiron","yves giraud cabantous","raymond sommer"],
        "Gran Premio de Francia": ["juan manuel fangio","luigi fagioli","jose froilan gonzalez","louis rosier","reg parnell","philippe etancelin","peter whitehead","louis chiron","yves giraud cabantous","raymond sommer"],
        "Gran Premio de Italia": ["giuseppe farina","juan manuel fangio","luigi fagioli","reg parnell","louis rosier","alberto ascari","philippe etancelin","peter whitehead","louis chiron","raymond sommer"]
    }, 
    1951: {
        "Gran Premio de Suiza": ["juan manuel fangio","giuseppe farina","luigi villoresi","piero taruffi","alberto ascari","felice bonetto","robert manzon","maurice trintignant","reg parnell","peter whitehead"],
        "Gran Premio de Indianápolis": ["lee wallard","bill holland","fred agabashian","troy ruttman","duane carter","johnnie parsons","jim rathmann","paul russo","sam hanks","jack mclaughlin"],
        "Gran Premio de Bélgica": ["giuseppe farina","juan manuel fangio","luigi villoresi","alberto ascari","felice bonetto","robert manzon","maurice trintignant","reg parnell","peter whitehead","roger laurent"],
        "Gran Premio de Francia": ["juan manuel fangio","luigi villoresi","alberto ascari","giuseppe farina","felice bonetto","robert manzon","maurice trintignant","reg parnell","peter whitehead","roger laurent"],
        "Gran Premio de Gran Bretaña": ["jose froilan gonzalez","juan manuel fangio","luigi villoresi","giuseppe farina","alberto ascari","felice bonetto","robert manzon","maurice trintignant","reg parnell","peter whitehead"],
        "Gran Premio de Alemania": ["alberto ascari","juan manuel fangio","giuseppe farina","luigi villoresi","felice bonetto","robert manzon","maurice trintignant","reg parnell","peter whitehead","roger laurent"],
        "Gran Premio de Italia": ["alberto ascari","juan manuel fangio","giuseppe farina","luigi villoresi","felice bonetto","robert manzon","maurice trintignant","reg parnell","peter whitehead","roger laurent"],
        "Gran Premio de España": ["juan manuel fangio","alberto ascari","giuseppe farina","luigi villoresi","felice bonetto","robert manzon","maurice trintignant","reg parnell","peter whitehead","roger laurent"]

    },
    1952: {
        "Gran Premio de Suiza": ["piero taruffi","rudi fischer","jean behra","roger laurent","peter whitehead","ken wharton","alan brown","eric brandon","rudolf schoeller","toni ulmen"],
        "Gran Premio de Indianápolis": ["troy ruttman","jim rathmann","sam hanks","bill vukovich","paul russo","duane carter","johnnie parsons","jimmy davies","eddie sack","bob sweikert"],
        "Gran Premio de Bélgica": ["alberto ascari","giuseppe farina","roberto mires","jean behra","roger laurent","ken wharton","peter whitehead","alan brown","eric brandon","rudolf schoeller"],
        "Gran Premio de Francia": ["alberto ascari","giuseppe farina","piero taruffi","roberto mires","jean behra","roger laurent","ken wharton","peter whitehead","alan brown","eric brandon"],
        "Gran Premio de Gran Bretaña": ["alberto ascari","giuseppe farina","piero taruffi","roberto mires","jean behra","roger laurent","ken wharton","peter whitehead","alan brown","eric brandon"],
        "Gran Premio de Alemania": ["alberto ascari","giuseppe farina","roberto mires","piero taruffi","jean behra","roger laurent","ken wharton","peter whitehead","alan brown","eric brandon"],
        "Gran Premio de Países Bajos": ["alberto ascari","giuseppe farina","piero taruffi","roberto mires","jean behra","roger laurent","ken wharton","peter whitehead","alan brown","eric brandon"],
        "Gran Premio de Italia": ["alberto ascari","giuseppe farina","piero taruffi","roberto mires","jean behra","roger laurent","ken wharton","peter whitehead","alan brown","eric brandon"]
    },
    1953: {
        "Gran Premio de Argentina": ["alberto ascari","luigi villoresi","jose froilan gonzalez","giuseppe farina","juan manuel fangio","roberto mires","onofre marimon","maurice trintignant","felice bonetto","roberto bonomi"],
        "Gran Premio de Países Bajos": ["alberto ascari","giuseppe farina","luigi villoresi","juan manuel fangio","roberto mires","maurice trintignant","felice bonetto","onofre marimon","peter whitehead","ken wharton"],
        "Gran Premio de Bélgica": ["alberto ascari","giuseppe farina","juan manuel fangio","luigi villoresi","maurice trintignant","felice bonetto","onofre marimon","peter whitehead","ken wharton","johnny claes"],
        "Gran Premio de Francia": ["mike hawthorn","juan manuel fangio","alberto ascari","giuseppe farina","luigi villoresi","maurice trintignant","felice bonetto","onofre marimon","peter whitehead","ken wharton"],
        "Gran Premio de Gran Bretaña": ["alberto ascari","juan manuel fangio","giuseppe farina","luigi villoresi","maurice trintignant","felice bonetto","onofre marimon","peter whitehead","ken wharton","reg parnell"],
        "Gran Premio de Alemania": ["alberto ascari","giuseppe farina","juan manuel fangio","maurice trintignant","felice bonetto","onofre marimon","peter whitehead","ken wharton","reg parnell","roger laurent"],
        "Gran Premio de Suiza": ["alberto ascari","juan manuel fangio","giuseppe farina","luigi villoresi","maurice trintignant","felice bonetto","onofre marimon","peter whitehead","ken wharton","roger laurent"],
        "Gran Premio de Italia": ["juan manuel fangio","alberto ascari","giuseppe farina","luigi villoresi","maurice trintignant","felice bonetto","onofre marimon","peter whitehead","ken wharton","roger laurent"]
    },
    1954: {
        "Gran Premio de Argentina": ["juan manuel fangio","giuseppe farina","jose froilan gonzalez","onofre marimon","nino farina","harry schell","roberto mieres","sergio mantovani","carlos menditeguy","jose froilan gonzalez"],
        "Gran Premio de Bélgica": ["juan manuel fangio","jose froilan gonzalez","mike hawthorn","jose froilan gonzalez","jean behra","trintignant","nino farina","stirling moss","onofre marimon","roberto mieres"],
        "Gran Premio de Francia": ["juan manuel fangio","karl kling","robert manzon","onofre marimon","jean behra","stirling moss","nino farina","jose froilan gonzalez","trintignant","roberto mieres"],
        "Gran Premio de Gran Bretaña": ["jose froilan gonzalez","mike hawthorn","onofre marimon","juan manuel fangio","nino farina","stirling moss","roberto mieres","trintignant","jean behra","harry schell"],
        "Gran Premio de Alemania": ["juan manuel fangio","jose froilan gonzalez","hans herrmann","karl kling","mike hawthorn","nino farina","trintignant","stirling moss","onofre marimon","roberto mieres"],
        "Gran Premio de Suiza": ["juan manuel fangio","jose froilan gonzalez","hans herrmann","karl kling","roberto mieres","stirling moss","nino farina","trintignant","jean behra","mike hawthorn"],
        "Gran Premio de Italia": ["juan manuel fangio","mike hawthorn","jose froilan gonzalez","nino farina","karl kling","hans herrmann","stirling moss","roberto mieres","trintignant","jean behra"],
        "Gran Premio de España": ["mike hawthorn","luigi musso","juan manuel fangio","roberto mieres","trintignant","juan manuel fangio","jose froilan gonzalez","stirling moss","nino farina","jean behra"],
    },
    1955: {
        "Gran Premio de Argentina": ["juan manuel fangio","jose froilan gonzalez","giuseppe farina","nino farina","trintignant","stirling moss","roberto mieres","jean behra","carlos menditeguy","harry schell"],
        "Gran Premio de Mónaco": ["trintignant","eugenio castellotti","cesare perdisa","jean behra","stirling moss","luigi villoresi","louis chiron","andre simon","juan manuel fangio","harry schell"],
        "Gran Premio de Bélgica": ["juan manuel fangio","stirling moss","giuseppe farina","paul frere","roberto mieres","jean behra","eugenio castellotti","andre simon","harry schell","carlos menditeguy"],
        "Gran Premio de los Países Bajos": ["juan manuel fangio","stirling moss","luigi musso","roberto mieres","jean behra","eugenio castellotti","harry schell","nino farina","andre simon","carlos menditeguy"],
        "Gran Premio de Gran Bretaña": ["stirling moss","juan manuel fangio","karl kling","piero taruffi","eugenio castellotti","mike hawthorn","luigi musso","roberto mieres","jean behra","harry schell"],
        "Gran Premio de Italia": ["juan manuel fangio","piero taruffi","eugenio castellotti","nino farina","roberto mieres","jean behra","luigi musso","cesare perdisa","stirling moss","harry schell"],
    },
    1956: {
        "Gran Premio de Argentina": ["juan manuel fangio","luigi musso","jean behra","nino farina","eugenio castellotti","jose froilan gonzalez","cesare perdisa","stirling moss","harry schell","roberto mieres"],
        "Gran Premio de Mónaco": ["stirling moss","peter collins","jean behra","juan manuel fangio","eugenio castellotti","cesare perdisa","nino farina","harry schell","roberto mieres","luigi musso"],
        "Gran Premio de Bélgica": ["peter collins","paul frere","cesare perdisa","stirling moss","jean behra","nino farina","eugenio castellotti","juan manuel fangio","harry schell","roberto mieres"],
        "Gran Premio de Francia": ["peter collins","eugenio castellotti","stirling moss","jean behra","nino farina","juan manuel fangio","harry schell","roberto mieres","cesare perdisa","luigi musso"],
        "Gran Premio de Gran Bretaña": ["juan manuel fangio","stirling moss","peter collins","jean behra","jack brabham","nino farina","eugenio castellotti","harry schell","cesare perdisa","roberto mieres"],
        "Gran Premio de Alemania": ["juan manuel fangio","stirling moss","peter collins","eugenio castellotti","jean behra","nino farina","jack brabham","harry schell","roberto mieres","cesare perdisa"],
        "Gran Premio de Italia": ["stirling moss","peter collins","ron flockhart","eugenio castellotti","juan manuel fangio","jean behra","nino farina","jack brabham","harry schell","cesare perdisa"],
    },
    1957: {
        "Gran Premio de Argentina": ["juan manuel fangio","jean behra","carlos menditeguy","harry schell","cesare perdisa","jack brabham","stirling moss","peter collins","mike hawthorn","luigi musso"],
        "Gran Premio de Mónaco": ["juan manuel fangio","tony brooks","masten gregory","stirling moss","peter collins","jack brabham","mike hawthorn","jean behra","harry schell","carlos menditeguy"],
        "Gran Premio de Francia": ["juan manuel fangio","luigi musso","peter collins","mike hawthorn","jean behra","stirling moss","jack brabham","harry schell","carlos menditeguy","cesare perdisa"],
        "Gran Premio de Gran Bretaña": ["stirling moss","tony brooks","jean behra","luigi musso","peter collins","mike hawthorn","jack brabham","harry schell","carlos menditeguy","juan manuel fangio"],
        "Gran Premio de Alemania": ["juan manuel fangio","mike hawthorn","peter collins","luigi musso","stirling moss","jean behra","jack brabham","harry schell","carlos menditeguy","cesare perdisa"],
        "Gran Premio de Pescara": ["stirling moss","juan manuel fangio","harry schell","luigi musso","peter collins","jack brabham","mike hawthorn","jean behra","carlos menditeguy","cesare perdisa"],
        "Gran Premio de Italia": ["stirling moss","juan manuel fangio","peter collins","mike hawthorn","luigi musso","jack brabham","jean behra","harry schell","carlos menditeguy","cesare perdisa"],
    },
    1958: {
        "Gran Premio de Argentina": ["stirling moss","luigi musso","mike hawthorn","juan manuel fangio","peter collins","jean behra","harry schell","cliff allison","jack brabham","roy salvadori"],
        "Gran Premio de Mónaco": ["trintignant","luigi musso","stirling moss","peter collins","jean behra","jack brabham","mike hawthorn","harry schell","cliff allison","roy salvadori"],
        "Gran Premio de los Países Bajos": ["stirling moss","harry schell","jean behra","ron flockhart","cliff allison","mike hawthorn","luigi musso","jack brabham","peter collins","roy salvadori"],
        "Gran Premio de Bélgica": ["tony brooks","mike hawthorn","stuart lewis evans","cliff allison","harry schell","luigi musso","stirling moss","jean behra","jack brabham","peter collins"],
        "Gran Premio de Francia": ["mike hawthorn","stirling moss","peter collins","luigi musso","tony brooks","jean behra","harry schell","cliff allison","jack brabham","roy salvadori"],
        "Gran Premio de Gran Bretaña": ["peter collins","mike hawthorn","roy salvadori","stirling moss","luigi musso","harry schell","jean behra","tony brooks","cliff allison","jack brabham"],
        "Gran Premio de Alemania": ["tony brooks","roy salvadori","stirling moss","mike hawthorn","peter collins","harry schell","jean behra","cliff allison","jack brabham","luigi musso"],
        "Gran Premio de Portugal": ["stirling moss","mike hawthorn","luigi musso","jean behra","peter collins","tony brooks","harry schell","cliff allison","jack brabham","roy salvadori"],
        "Gran Premio de Italia": ["tony brooks","mike hawthorn","phil hill","stirling moss","luigi musso","harry schell","jean behra","jack brabham","cliff allison","roy salvadori"],
        "Gran Premio de Marruecos": ["stirling moss","mike hawthorn","phil hill","jo bonnier","tony brooks","harry schell","jean behra","cliff allison","jack brabham","roy salvadori"],
    },
    1959: {
        "Gran Premio de Mónaco": ["jack brabham","tony brooks","masten gregory","phil hill","stirling moss","bruce mclaren","jo bonnier","harry schell","cliff allison","roy salvadori"],
        "Gran Premio de Indianapolis": ["rodger ward","jim rathmann","johnny thomson","tony bettenhausen","paul goldsmith","johnny boyd","eddie johnson","jim mcwitthy","troy ruttman","jim hurtubise"],
        "Gran Premio de Francia": ["tony brooks","phil hill","jack brabham","olivier gendebien","bruce mclaren","masten gregory","jo bonnier","stirling moss","harry schell","cliff allison"],
        "Gran Premio de Gran Bretaña": ["jack brabham","stirling moss","bruce mclaren","masten gregory","tony brooks","phil hill","jo bonnier","harry schell","cliff allison","roy salvadori"],
        "Gran Premio de Alemania": ["tony brooks","jack brabham","masten gregory","stirling moss","bruce mclaren","jo bonnier","phil hill","harry schell","cliff allison","roy salvadori"],
        "Gran Premio de Portugal": ["stirling moss","masten gregory","jack brabham","tony brooks","masten gregory","jo bonnier","bruce mclaren","phil hill","harry schell","cliff allison"],
        "Gran Premio de Italia": ["stirling moss","phil hill","jack brabham","tony brooks","masten gregory","jo bonnier","bruce mclaren","harry schell","cliff allison","roy salvadori"],
        "Gran Premio de Estados Unidos": ["bruce mclaren","trintignant","tony brooks","jack brabham","stirling moss","jo bonnier","masten gregory","phil hill","harry schell","cliff allison"],
    },
    1960: {
        "Gran Premio de Argentina": ["bruce mclaren","cliff allison","stirling moss","innes ireland","trintignant","jo bonnier","jack brabham","phil hill","harry schell","tony brooks"],
        "Gran Premio de Mónaco": ["stirling moss","tony brooks","bruce mclaren","phil hill","jo bonnier","richie ginther","jack brabham","innes ireland","cliff allison","harry schell"],
        "Gran Premio de Indianapolis": ["jim rathmann","rodger ward","paul goldsmith","lloyd ruby","jim hurtubise","johnny thomson","tony bettenhausen","eddie sachs","don branson","jimmy daywalt"],
        "Gran Premio de los Países Bajos": ["jack brabham","innes ireland","stirling moss","phil hill","jo bonnier","bruce mclaren","cliff allison","tony brooks","henry taylor","jim clark"],
        "Gran Premio de Bélgica": ["jack brabham","bruce mclaren","stirling moss","innes ireland","phil hill","jo bonnier","chris bristow","michael taylor","cliff allison","tony brooks"],
        "Gran Premio de Francia": ["jack brabham","olivier gendebien","bruce mclaren","henry taylor","innes ireland","jim clark","phil hill","jo bonnier","stirling moss","cliff allison"],
        "Gran Premio de Gran Bretaña": ["jack brabham","john surtees","innes ireland","bruce mclaren","tony brooks","jim clark","phil hill","jo bonnier","stirling moss","cliff allison"],
        "Gran Premio de Portugal": ["jack brabham","bruce mclaren","jim clark","innes ireland","tony brooks","phil hill","jo bonnier","stirling moss","cliff allison","henry taylor"],
        "Gran Premio de Italia": ["phil hill","richie ginther","willy mairesse","bruce mclaren","phil hill","jim clark","innes ireland","jo bonnier","jack brabham","stirling moss"],
        "Gran Premio de Estados Unidos": ["stirling moss","innes ireland","bruce mclaren","jack brabham","jim clark","phil hill","jo bonnier","tony brooks","cliff allison","henry taylor"],
    },
    1961: {
        "Gran Premio de Mónaco": ["stirling moss","richie ginther","phil hill","dan gurney","bruce mclaren","graham hill","gino munaron","jo bonnier","tony brooks","henry taylor"],
        "Gran Premio de los Países Bajos": ["von trips","phil hill","jim clark","stirling moss","richie ginther","innes ireland","dan gurney","henry taylor","jo bonnier","bruce mclaren"],
        "Gran Premio de Bélgica": ["phil hill","von trips","richie ginther","olivier gendebien","john surtees","willy mairesse","bruce mclaren","jim clark","innes ireland","jo bonnier"],
        "Gran Premio de Francia": ["giancarlo baghetti","dan gurney","phil hill","von trips","richie ginther","innes ireland","jim clark","bruce mclaren","jo bonnier","ron flockhart"],
        "Gran Premio de Gran Bretaña": ["von trips","phil hill","richie ginther","dan gurney","tony brooks","bruce mclaren","jim clark","innes ireland","jo bonnier","ron flockhart"],
        "Gran Premio de Alemania": ["stirling moss","von trips","phil hill","richie ginther","jim clark","john surtees","innes ireland","bruce mclaren","jo bonnier","dan gurney"],
        "Gran Premio de Italia": ["phil hill","dan gurney","richie ginther","innes ireland","bruce mclaren","jim clark","tony brooks","jo bonnier","ron flockhart","willy mairesse"],
        "Gran Premio de Estados Unidos": ["innes ireland","dan gurney","tony brooks","john surtees","jo bonnier","bruce mclaren","ronnie bucknum","jim hall","jack brabham","stirling moss"],
    },
    1962: {
        "Gran Premio de los Países Bajos": ["graham hill","trevor taylor","phil hill","john surtees","tony maggs","carel godin de beaufort","jack brabham","stirling moss","bruce mclaren","jim clark"],
        "Gran Premio de Mónaco": ["bruce mclaren","phil hill","jack brabham","john surtees","tony maggs","graham hill","jim clark","richie ginther","innes ireland","trevor taylor"],
        "Gran Premio de Bélgica": ["jim clark","graham hill","phil hill","john surtees","tony maggs","richie ginther","jack brabham","bruce mclaren","trevor taylor","innes ireland"],
        "Gran Premio de Francia": ["dan gurney","tony maggs","richie ginther","jim clark","jack brabham","graham hill","phil hill","john surtees","bruce mclaren","trevor taylor"],
        "Gran Premio de Gran Bretaña": ["jim clark","john surtees","bruce mclaren","jack brabham","tony maggs","graham hill","richie ginther","trevor taylor","phil hill","innes ireland"],
        "Gran Premio de Alemania": ["graham hill","john surtees","dan gurney","bruce mclaren","jim clark","tony maggs","richie ginther","phil hill","jack brabham","trevor taylor"],
        "Gran Premio de Italia": ["graham hill","richie ginther","bruce mclaren","john surtees","dan gurney","tony maggs","jack brabham","jim clark","trevor taylor","innes ireland"],
        "Gran Premio de Estados Unidos": ["jim clark","graham hill","bruce mclaren","john surtees","tony maggs","richie ginther","jack brabham","dan gurney","innes ireland","trevor taylor"],
        "Gran Premio de Sudáfrica": ["graham hill","bruce mclaren","tony maggs","jack brabham","richie ginther","jim clark","john surtees","innes ireland","trevor taylor","dan gurney"],
    },
    1963: {
        "Gran Premio de Mónaco": ["graham hill","richie ginther","bruce mclaren","john surtees","jim clark","tony maggs","jack brabham","innes ireland","trevor taylor","dan gurney"],
        "Gran Premio de Bélgica": ["jim clark","bruce mclaren","dan gurney","richie ginther","graham hill","jack brabham","tony maggs","john surtees","trevor taylor","innes ireland"],
        "Gran Premio de los Países Bajos": ["jim clark","dan gurney","john surtees","richie ginther","graham hill","bruce mclaren","tony maggs","jack brabham","trevor taylor","innes ireland"],
        "Gran Premio de Francia": ["jim clark","tony maggs","graham hill","jack brabham","richie ginther","dan gurney","john surtees","bruce mclaren","trevor taylor","innes ireland"],
        "Gran Premio de Gran Bretaña": ["jim clark","john surtees","graham hill","richie ginther","dan gurney","tony maggs","jack brabham","bruce mclaren","trevor taylor","innes ireland"],
        "Gran Premio de Alemania": ["john surtees","jim clark","richie ginther","graham hill","dan gurney","tony maggs","jack brabham","bruce mclaren","trevor taylor","innes ireland"],
        "Gran Premio de Italia": ["jim clark","richie ginther","bruce mclaren","graham hill","john surtees","dan gurney","tony maggs","jack brabham","trevor taylor","innes ireland"],
        "Gran Premio de Estados Unidos": ["graham hill","richie ginther","jim clark","dan gurney","jack brabham","tony maggs","bruce mclaren","trevor taylor","john surtees","innes ireland"],
        "Gran Premio de México": ["jim clark","jack brabham","richie ginther","innes ireland","graham hill","dan gurney","john surtees","bruce mclaren","tony maggs","trevor taylor"],
        "Gran Premio de Sudáfrica": ["jim clark","dan gurney","graham hill","tony maggs","john surtees","richie ginther","jack brabham","bruce mclaren","trevor taylor","innes ireland"],
    },
    1964: {
        "Gran Premio de Mónaco": ["graham hill","richie ginther","peter arundell","jack brabham","jim clark","bruce mclaren","dan gurney","john surtees","mike spence","tony maggs"],
        "Gran Premio de los Países Bajos": ["jim clark","john surtees","peter arundell","richie ginther","bruce mclaren","graham hill","dan gurney","jack brabham","tony maggs","mike spence"],
        "Gran Premio de Bélgica": ["jim clark","bruce mclaren","jack brabham","richie ginther","graham hill","peter arundell","john surtees","dan gurney","tony maggs","mike spence"],
        "Gran Premio de Francia": ["dan gurney","graham hill","jack brabham","richie ginther","jim clark","peter arundell","john surtees","bruce mclaren","tony maggs","mike spence"],
        "Gran Premio de Gran Bretaña": ["jim clark","graham hill","john surtees","jack brabham","dan gurney","richie ginther","peter arundell","bruce mclaren","tony maggs","mike spence"],
        "Gran Premio de Alemania": ["john surtees","graham hill","lorenzo bandini","jim clark","richie ginther","jack brabham","dan gurney","bruce mclaren","tony maggs","mike spence"],
        "Gran Premio de Austria": ["lorenzo bandini","richie ginther","bob anderson","tony maggs","jack brabham","dan gurney","jim clark","graham hill","john surtees","bruce mclaren"],
        "Gran Premio de Italia": ["john surtees","bruce mclaren","lorenzo bandini","richie ginther","jim clark","dan gurney","graham hill","jack brabham","tony maggs","mike spence"],
        "Gran Premio de Estados Unidos": ["graham hill","john surtees","jim clark","lorenzo bandini","richie ginther","dan gurney","jack brabham","bruce mclaren","tony maggs","mike spence"],
        "Gran Premio de México": ["dan gurney","john surtees","lorenzo bandini","mike spence","jack brabham","jim clark","richie ginther","graham hill","bruce mclaren","tony maggs"],
    },
    1965: {
        "Gran Premio de Sudáfrica": ["jim clark","john surtees","graham hill","mike spence","jack brabham","dan gurney","bruce mclaren","richie ginther","jackie stewart","tony maggs"],
        "Gran Premio de Mónaco": ["graham hill","lorenzo bandini","jackie stewart","john surtees","mike spence","bruce mclaren","dan gurney","jim clark","richie ginther","jack brabham"],
        "Gran Premio de Bélgica": ["jim clark","jackie stewart","bruce mclaren","graham hill","richie ginther","john surtees","mike spence","dan gurney","jack brabham","tony maggs"],
        "Gran Premio de Francia": ["jim clark","jackie stewart","john surtees","dan gurney","mike spence","richie ginther","graham hill","bruce mclaren","jack brabham","tony maggs"],
        "Gran Premio de Gran Bretaña": ["jim clark","graham hill","john surtees","mike spence","dan gurney","richie ginther","jackie stewart","bruce mclaren","jack brabham","tony maggs"],
        "Gran Premio de los Países Bajos": ["jim clark","jackie stewart","dan gurney","john surtees","graham hill","richie ginther","mike spence","bruce mclaren","jack brabham","tony maggs"],
        "Gran Premio de Alemania": ["jim clark","graham hill","dan gurney","john surtees","richie ginther","jackie stewart","bruce mclaren","mike spence","jack brabham","tony maggs"],
        "Gran Premio de Italia": ["jackie stewart","graham hill","dan gurney","john surtees","richie ginther","jim clark","mike spence","bruce mclaren","jack brabham","tony maggs"],
        "Gran Premio de Estados Unidos": ["graham hill","dan gurney","john surtees","jackie stewart","jim clark","richie ginther","mike spence","bruce mclaren","jack brabham","tony maggs"],
        "Gran Premio de México": ["richie ginther","dan gurney","mike spence","jackie stewart","jim clark","john surtees","graham hill","bruce mclaren","jack brabham","tony maggs"],
    },
    1966: {
        "Gran Premio de Mónaco": ["jackie stewart","lorenzo bandini","graham hill","bob bondurant","bruce mclaren","jack brabham","dan gurney","john surtees","richie ginther","mike spence"],
        "Gran Premio de Bélgica": ["john surtees","jochen rindt","lorenzo bandini","jack brabham","graham hill","joakim bonnier","dan gurney","bruce mclaren","richie ginther","mike spence"],
        "Gran Premio de Francia": ["jack brabham","mike parkes","denny hulme","jochen rindt","graham hill","jackie stewart","dan gurney","john surtees","bruce mclaren","richie ginther"],
        "Gran Premio de Gran Bretaña": ["jack brabham","denny hulme","graham hill","jim clark","jochen rindt","bruce mclaren","jackie stewart","dan gurney","john surtees","richie ginther"],
        "Gran Premio de los Países Bajos": ["jack brabham","graham hill","jim clark","jochen rindt","denny hulme","bruce mclaren","jackie stewart","dan gurney","john surtees","richie ginther"],
        "Gran Premio de Alemania": ["jack brabham","john surtees","jochen rindt","graham hill","denny hulme","jackie stewart","dan gurney","bruce mclaren","jim clark","richie ginther"],
        "Gran Premio de Italia": ["ludovico scarfiotti","mike parkes","denny hulme","jochen rindt","jack brabham","graham hill","jackie stewart","dan gurney","bruce mclaren","jim clark"],
        "Gran Premio de Estados Unidos": ["jim clark","jochen rindt","jack brabham","john surtees","denny hulme","graham hill","jackie stewart","dan gurney","bruce mclaren","richie ginther"],
        "Gran Premio de México": ["john surtees","jack brabham","denny hulme","jochen rindt","jim clark","graham hill","jackie stewart","dan gurney","bruce mclaren","richie ginther"],
    },
    1967: {
        "Gran Premio de Sudáfrica": ["pedro rodriguez","john love","john surtees","denny hulme","jack brabham","jim clark","mike spence","jackie stewart","graham hill","dan gurney"],
        "Gran Premio de Mónaco": ["denny hulme","graham hill","chris amon","dan gurney","jim clark","jack brabham","jo siffert","jackie stewart","john surtees","mike spence"],
        "Gran Premio de los Países Bajos": ["jim clark","jack brabham","denny hulme","dan gurney","chris amon","jochen rindt","mike spence","graham hill","jackie stewart","jo siffert"],
        "Gran Premio de Bélgica": ["dan gurney","jim clark","jack brabham","denny hulme","chris amon","graham hill","jackie stewart","jochen rindt","jo siffert","mike spence"],
        "Gran Premio de Francia": ["jack brabham","denny hulme","dan gurney","jo siffert","jim clark","chris amon","graham hill","jackie stewart","jochen rindt","mike spence"],
        "Gran Premio de Gran Bretaña": ["jim clark","denny hulme","chris amon","jack brabham","dan gurney","jo siffert","graham hill","jackie stewart","jochen rindt","mike spence"],
        "Gran Premio de Alemania": ["denny hulme","jack brabham","dan gurney","chris amon","jochen rindt","jim clark","jo siffert","graham hill","jackie stewart","mike spence"],
        "Gran Premio de Canadá": ["jack brabham","denny hulme","dan gurney","jo siffert","jochen rindt","jim clark","chris amon","graham hill","jackie stewart","mike spence"],
        "Gran Premio de Italia": ["john surtees","jack brabham","jim clark","jochen rindt","denny hulme","dan gurney","chris amon","jo siffert","graham hill","jackie stewart"],
        "Gran Premio de Estados Unidos": ["jim clark","graham hill","denny hulme","dan gurney","jo siffert","jochen rindt","jack brabham","chris amon","jackie stewart","mike spence"],
        "Gran Premio de México": ["jim clark","jack brabham","denny hulme","jochen rindt","dan gurney","jo siffert","chris amon","graham hill","jackie stewart","mike spence"],
    },
    1968: {
        "Gran Premio de Sudáfrica": ["jim clark","graham hill","jochen rindt","chris amon","denny hulme","jackie stewart","john surtees","jack brabham","jo siffert","bruce mclaren"],
        "Gran Premio de España": ["graham hill","denny hulme","brian redman","john surtees","jochen rindt","chris amon","jackie stewart","jack brabham","jo siffert","bruce mclaren"],
        "Gran Premio de Mónaco": ["graham hill","richard attwood","lucien bianchi","jochen rindt","chris amon","denny hulme","jackie stewart","john surtees","jack brabham","jo siffert"],
        "Gran Premio de Bélgica": ["bruce mclaren","pedro rodriguez","jackie ickx","jackie stewart","jochen rindt","john surtees","denny hulme","chris amon","jack brabham","jo siffert"],
        "Gran Premio de los Países Bajos": ["jackie stewart","jean pierre beltoise","pedro rodriguez","jackie ickx","jochen rindt","denny hulme","chris amon","john surtees","jack brabham","jo siffert"],
        "Gran Premio de Francia": ["jackie ickx","john surtees","jackie stewart","pedro rodriguez","jochen rindt","denny hulme","chris amon","jack brabham","jo siffert","bruce mclaren"],
        "Gran Premio de Gran Bretaña": ["jo siffert","chris amon","jackie stewart","jackie ickx","jochen rindt","denny hulme","john surtees","jack brabham","bruce mclaren","pedro rodriguez"],
        "Gran Premio de Alemania": ["jackie stewart","graham hill","jochen rindt","jackie ickx","jack brabham","denny hulme","jo siffert","chris amon","john surtees","pedro rodriguez"],
        "Gran Premio de Italia": ["denny hulme","johnny servoz gavin","jackie ickx","jochen rindt","jackie stewart","graham hill","jo siffert","chris amon","jack brabham","bruce mclaren"],
        "Gran Premio de Canadá": ["denny hulme","bruce mclaren","pedro rodriguez","graham hill","jackie stewart","jochen rindt","jackie ickx","jo siffert","chris amon","jack brabham"],
        "Gran Premio de Estados Unidos": ["jackie stewart","graham hill","john surtees","pedro rodriguez","denny hulme","bruce mclaren","jochen rindt","jackie ickx","jo siffert","chris amon"],
        "Gran Premio de México": ["graham hill","bruce mclaren","jackie oliver","pedro rodriguez","denny hulme","jackie ickx","jo siffert","chris amon","jack brabham","jackie stewart"],
    },
    1969: {
        "Gran Premio de Sudáfrica": ["jackie stewart","graham hill","denny hulme","jochen rindt","jean pierre beltoise","jo siffert","bruce mclaren","jackie ickx","jack brabham","chris amon"],
        "Gran Premio de España": ["jackie stewart","bruce mclaren","jean pierre beltoise","denny hulme","jochen rindt","graham hill","jackie ickx","jo siffert","jack brabham","chris amon"],
        "Gran Premio de Mónaco": ["graham hill","piers courage","jo siffert","jean pierre beltoise","denny hulme","jackie stewart","jochen rindt","bruce mclaren","jackie ickx","jack brabham"],
        "Gran Premio de los Países Bajos": ["jackie stewart","jo siffert","chris amon","jochen rindt","denny hulme","jean pierre beltoise","jackie ickx","graham hill","jack brabham","bruce mclaren"],
        "Gran Premio de Francia": ["jackie stewart","francois cevert","jochen rindt","jean pierre beltoise","denny hulme","graham hill","jo siffert","jackie ickx","jack brabham","chris amon"],
        "Gran Premio de Gran Bretaña": ["jackie stewart","jackie ickx","bruce mclaren","jochen rindt","denny hulme","jean pierre beltoise","graham hill","jo siffert","jack brabham","chris amon"],
        "Gran Premio de Alemania": ["jackie ickx","jackie stewart","bruce mclaren","jochen rindt","denny hulme","jean pierre beltoise","graham hill","jo siffert","jack brabham","chris amon"],
        "Gran Premio de Italia": ["jackie stewart","jochen rindt","jean pierre beltoise","bruce mclaren","piers courage","denny hulme","graham hill","jo siffert","jackie ickx","jack brabham"],
        "Gran Premio de Canadá": ["jackie ickx","jochen rindt","jack brabham","denny hulme","jean pierre beltoise","bruce mclaren","jackie stewart","graham hill","jo siffert","chris amon"],
        "Gran Premio de Estados Unidos": ["jochen rindt","piers courage","john surtees","peter gethin","jack brabham","jackie stewart","denny hulme","graham hill","jo siffert","jackie ickx"],
        "Gran Premio de México": ["denny hulme","jackie ickx","jackie stewart","jack brabham","jochen rindt","piers courage","jean pierre beltoise","bruce mclaren","graham hill","jo siffert"],
    },
    1970: {
        "Gran Premio de Sudáfrica": ["jack brabham","denny hulme","jackie stewart","jean pierre beltoise","jochen rindt","john miles","mario andretti","graham hill","jackie ickx","chris amon"],
        "Gran Premio de España": ["jackie stewart","bruce mclaren","mario andretti","graham hill","jackie ickx","jochen rindt","jean pierre beltoise","denny hulme","jack brabham","emerson fittipaldi"],
        "Gran Premio de Mónaco": ["jochen rindt","jackie ickx","jean pierre beltoise","henri pescarolo","graham hill","denny hulme","jack brabham","jackie stewart","emerson fittipaldi","rolf stommelen"],
        "Gran Premio de Bélgica": ["pedro rodriguez","chris amon","ignazio giunti","denny hulme","jean pierre beltoise","jochen rindt","jackie ickx","jackie stewart","emerson fittipaldi","jack brabham"],
        "Gran Premio de los Países Bajos": ["jochen rindt","jackie ickx","jackie stewart","emerson fittipaldi","clay regazzoni","rolf stommelen","pedro rodriguez","jack brabham","jean pierre beltoise","denny hulme"],
        "Gran Premio de Francia": ["jochen rindt","clay regazzoni","chris amon","jack brabham","denny hulme","jackie ickx","emerson fittipaldi","jean pierre beltoise","jackie stewart","pedro rodriguez"],
        "Gran Premio de Gran Bretaña": ["jochen rindt","jack brabham","denny hulme","clay regazzoni","chris amon","rolf stommelen","pedro rodriguez","emerson fittipaldi","jackie ickx","jackie stewart"],
        "Gran Premio de Alemania": ["jochen rindt","jackie ickx","denny hulme","emerson fittipaldi","rolf stommelen","pedro rodriguez","clay regazzoni","jack brabham","jackie stewart","chris amon"],
        "Gran Premio de Austria": ["jackie ickx","clay regazzoni","rolf stommelen","pedro rodriguez","emerson fittipaldi","graham hill","denny hulme","jochen rindt","jack brabham","jackie stewart"],
        "Gran Premio de Italia": ["clay regazzoni","jackie stewart","jean pierre beltoise","denny hulme","rolf stommelen","emerson fittipaldi","pedro rodriguez","jack brabham","jackie ickx","chris amon"],
        "Gran Premio de Canadá": ["jackie ickx","clay regazzoni","chris amon","peter gethin","emerson fittipaldi","graham hill","denny hulme","john miles","rolf stommelen","jackie stewart"],
        "Gran Premio de Estados Unidos": ["emerson fittipaldi","pedro rodriguez","reine wisell","jack brabham","denny hulme","clay regazzoni","chris amon","jackie ickx","graham hill","rolf stommelen"],
        "Gran Premio de México": ["jackie ickx","clay regazzoni","denny hulme","chris amon","pedro rodriguez","emerson fittipaldi","reine wisell","rolf stommelen","graham hill","jack brabham"],
    },
    1971: {
        "Gran Premio de Sudáfrica": ["mario andretti","jackie stewart","clay regazzoni","reine wisell","rolf stommelen","henri pescarolo","graham hill","john surtees","denny hulme","jackie oliver"],
        "Gran Premio de España": ["jackie stewart","jacky ickx","chris amon","pedro rodriguez","denny hulme","rolf stommelen","jean pierre beltoise","graham hill","reine wisell","peter gethin"],
        "Gran Premio de Mónaco": ["jackie stewart","ronnie peterson","jacky ickx","reine wisell","denny hulme","chris amon","mark donohue","rolf stommelen","graham hill","pedro rodriguez"],
        "Gran Premio de Países Bajos": ["jackie stewart","pedro rodriguez","clay regazzoni","jacky ickx","reine wisell","ronnie peterson","denny hulme","chris amon","rolf stommelen","andrea de adamich"],
        "Gran Premio de Francia": ["jackie stewart","francois cevert","emerson fittipaldi","mike hailwood","clay regazzoni","reine wisell","jacky ickx","peter gethin","rolf stommelen","denny hulme"],
        "Gran Premio de Gran Bretaña": ["jo siffert","francois cevert","emerson fittipaldi","mike hailwood","graham hill","clay regazzoni","jackie stewart","reine wisell","peter gethin","john surtees"],
        "Gran Premio de Alemania": ["jackie stewart","francois cevert","clay regazzoni","mario andretti","ronnie peterson","rolf stommelen","howden ganley","tim schenken","reine wisell","pedro rodriguez"],
        "Gran Premio de Austria": ["jo siffert","emerson fittipaldi","tim schenken","reine wisell","jacky ickx","francois cevert","clay regazzoni","chris amon","denny hulme","andrea de adamich"],
        "Gran Premio de Italia": ["peter gethin","ronnie peterson","francois cevert","mike hailwood","howden ganley","rolf stommelen","chris amon","clay regazzoni","reine wisell","jacky ickx"],
        "Gran Premio de Canadá": ["jackie stewart","ronnie peterson","mark donohue","denny hulme","reine wisell","francois cevert","jo siffert","clay regazzoni","peter gethin","chris amon"],
        "Gran Premio de Estados Unidos": ["francois cevert","jo siffert","ronnie peterson","emerson fittipaldi","reine wisell","jackie stewart","clay regazzoni","mark donohue","howden ganley","denny hulme"],
    },
    1972: {
        "Gran Premio de Argentina": ["jackie stewart","denny hulme","jacky ickx","ronnie peterson","emerson fittipaldi","clay regazzoni","carlos reutemann","howden ganley","tim schenken","peter revson"],
        "Gran Premio de Sudáfrica": ["denny hulme","emerson fittipaldi","peter revson","mario andretti","jacky ickx","mike hailwood","ronnie peterson","clay regazzoni","tim schenken","howden ganley"],
        "Gran Premio de España": ["emerson fittipaldi","jacky ickx","clay regazzoni","andrea de adamich","carlos reutemann","ronnie peterson","peter revson","denny hulme","jackie stewart","rolf stommelen"],
        "Gran Premio de Mónaco": ["jean pierre beltoise","jacky ickx","emerson fittipaldi","jackie stewart","brian redman","chris amon","carlos reutemann","ronnie peterson","denny hulme","tim schenken"],
        "Gran Premio de Bélgica": ["emerson fittipaldi","francois cevert","denny hulme","mike hailwood","jacky ickx","clay regazzoni","jackie stewart","carlos reutemann","ronnie peterson","howden ganley"],
        "Gran Premio de Francia": ["jackie stewart","emerson fittipaldi","chris amon","francois cevert","reine wisell","denny hulme","jacky ickx","clay regazzoni","howden ganley","carlos reutemann"],
        "Gran Premio de Gran Bretaña": ["emerson fittipaldi","jackie stewart","peter revson","chris amon","denny hulme","carlos reutemann","francois cevert","clay regazzoni","ronnie peterson","mike hailwood"],
        "Gran Premio de Alemania": ["jacky ickx","clay regazzoni","ronnie peterson","denny hulme","jackie stewart","emerson fittipaldi","carlos reutemann","francois cevert","peter revson","rolf stommelen"],
        "Gran Premio de Austria": ["emerson fittipaldi","denny hulme","peter revson","carlos reutemann","clay regazzoni","jacky ickx","ronnie peterson","jackie stewart","francois cevert","howden ganley"],
        "Gran Premio de Italia": ["emerson fittipaldi","mike hailwood","denny hulme","peter revson","ronnie peterson","jacky ickx","jackie stewart","carlos reutemann","clay regazzoni","francois cevert"],
        "Gran Premio de Canadá": ["jackie stewart","peter revson","denny hulme","jacky ickx","emerson fittipaldi","clay regazzoni","francois cevert","carlos reutemann","ronnie peterson","mike hailwood"],
        "Gran Premio de Estados Unidos": ["jackie stewart","francois cevert","denny hulme","ronnie peterson","jacky ickx","emerson fittipaldi","peter revson","clay regazzoni","carlos reutemann","mike hailwood"],
    },
    1973: {
        "Gran Premio de Argentina": ["emerson fittipaldi","francois cevert","denny hulme","jackie stewart","ronnie peterson","carlos reutemann","jacky ickx","clay regazzoni","carlos pace","arturo merzario"],
        "Gran Premio de Brasil": ["emerson fittipaldi","jacky ickx","denny hulme","jackie stewart","francois cevert","peter revson","ronnie peterson","carlos reutemann","clay regazzoni","carlos pace"],
        "Gran Premio de Sudáfrica": ["jackie stewart","peter revson","emerson fittipaldi","jacky ickx","francois cevert","denny hulme","ronnie peterson","clay regazzoni","carlos reutemann","mike hailwood"],
        "Gran Premio de España": ["emerson fittipaldi","francois cevert","george follmer","jacky ickx","jean pierre beltoise","denny hulme","jackie stewart","carlos reutemann","carlos pace","arturo merzario"],
        "Gran Premio de Bélgica": ["francois cevert","emerson fittipaldi","jacky ickx","denny hulme","jackie stewart","ronnie peterson","carlos reutemann","clay regazzoni","niki lauda","carlos pace"],
        "Gran Premio de Mónaco": ["jacky ickx","emerson fittipaldi","ronnie peterson","jackie stewart","francois cevert","carlos reutemann","denny hulme","niki lauda","clay regazzoni","jean pierre beltoise"],
        "Gran Premio de Suecia": ["denny hulme","ronnie peterson","francois cevert","jacky ickx","emerson fittipaldi","jackie stewart","carlos reutemann","clay regazzoni","niki lauda","jean pierre beltoise"],
        "Gran Premio de Francia": ["ronnie peterson","francois cevert","carlos reutemann","emerson fittipaldi","jacky ickx","denny hulme","jackie stewart","clay regazzoni","niki lauda","jean pierre beltoise"],
        "Gran Premio de Gran Bretaña": ["peter revson","ronnie peterson","denny hulme","emerson fittipaldi","jackie stewart","francois cevert","jacky ickx","carlos reutemann","clay regazzoni","niki lauda"],
        "Gran Premio de Países Bajos": ["jackie stewart","ronnie peterson","francois cevert","jacky ickx","emerson fittipaldi","denny hulme","carlos reutemann","clay regazzoni","niki lauda","jean pierre beltoise"],
        "Gran Premio de Alemania": ["jacky ickx","jackie stewart","ronnie peterson","francois cevert","carlos reutemann","emerson fittipaldi","denny hulme","clay regazzoni","niki lauda","andrea de adamich"],
        "Gran Premio de Austria": ["ronnie peterson","emerson fittipaldi","carlos reutemann","denny hulme","jacky ickx","jackie stewart","francois cevert","clay regazzoni","niki lauda","jean pierre beltoise"],
        "Gran Premio de Italia": ["ronnie peterson","emerson fittipaldi","peter revson","jacky ickx","francois cevert","denny hulme","jackie stewart","carlos reutemann","clay regazzoni","niki lauda"],
        "Gran Premio de Canadá": ["peter revson","emerson fittipaldi","jacky ickx","jackie stewart","denny hulme","ronnie peterson","carlos reutemann","clay regazzoni","niki lauda","jean pierre beltoise"],
        "Gran Premio de Estados Unidos": ["ronnie peterson","jacky ickx","denny hulme","emerson fittipaldi","carlos reutemann","jackie stewart","francois cevert","clay regazzoni","niki lauda","jean pierre beltoise"],
    },
    1974: {
        "Gran Premio de Argentina": ["denny hulme","niki lauda","clay regazzoni","mike hailwood","emerson fittipaldi","carlos reutemann","jacky ickx","ronnie peterson","jean pierre beltoise","carlos pace"],
        "Gran Premio de Brasil": ["emerson fittipaldi","clay regazzoni","jacky ickx","niki lauda","denny hulme","carlos reutemann","ronnie peterson","jean pierre beltoise","carlos pace","arturo merzario"],
        "Gran Premio de Sudáfrica": ["carlos reutemann","jean pierre beltoise","mike hailwood","peter revson","denny hulme","jacky ickx","clay regazzoni","niki lauda","emerson fittipaldi","carlos pace"],
        "Gran Premio de España": ["niki lauda","clay regazzoni","emerson fittipaldi","hans joachim stuck","jacky ickx","ronnie peterson","denny hulme","carlos reutemann","jean pierre beltoise","carlos pace"],
        "Gran Premio de Bélgica": ["emerson fittipaldi","niki lauda","jody scheckter","clay regazzoni","denny hulme","carlos reutemann","ronnie peterson","jacky ickx","jean pierre beltoise","carlos pace"],
        "Gran Premio de Mónaco": ["ronnie peterson","jody scheckter","jean pierre beltoise","clay regazzoni","niki lauda","emerson fittipaldi","denny hulme","carlos reutemann","jacky ickx","carlos pace"],
        "Gran Premio de Suecia": ["jody scheckter","patrick depailler","james hunt","clay regazzoni","niki lauda","emerson fittipaldi","denny hulme","carlos reutemann","ronnie peterson","jacky ickx"],
        "Gran Premio de Países Bajos": ["niki lauda","clay regazzoni","emerson fittipaldi","jody scheckter","hans joachim stuck","denny hulme","carlos reutemann","ronnie peterson","jacky ickx","carlos pace"],
        "Gran Premio de Francia": ["ronnie peterson","niki lauda","emerson fittipaldi","carlos reutemann","denny hulme","clay regazzoni","jody scheckter","jacky ickx","jean pierre beltoise","carlos pace"],
        "Gran Premio de Gran Bretaña": ["jody scheckter","emerson fittipaldi","jacky ickx","niki lauda","clay regazzoni","denny hulme","ronnie peterson","carlos reutemann","jean pierre beltoise","carlos pace"],
        "Gran Premio de Alemania": ["clay regazzoni","jody scheckter","jacky ickx","emerson fittipaldi","carlos reutemann","denny hulme","niki lauda","ronnie peterson","jean pierre beltoise","hans joachim stuck"],
        "Gran Premio de Austria": ["carlos reutemann","denny hulme","niki lauda","james hunt","clay regazzoni","jody scheckter","emerson fittipaldi","ronnie peterson","jacky ickx","jean pierre beltoise"],
        "Gran Premio de Italia": ["ronnie peterson","emerson fittipaldi","jody scheckter","niki lauda","denny hulme","clay regazzoni","carlos reutemann","jacky ickx","jean pierre beltoise","carlos pace"],
        "Gran Premio de Canadá": ["emerson fittipaldi","clay regazzoni","denny hulme","niki lauda","jody scheckter","jacky ickx","ronnie peterson","carlos reutemann","jean pierre beltoise","carlos pace"],
        "Gran Premio de Estados Unidos": ["carlos reutemann","carlos pace","james hunt","emerson fittipaldi","ronnie peterson","niki lauda","clay regazzoni","jody scheckter","denny hulme","jacky ickx"],
    },
    1975: {
        "Gran Premio de Argentina": ["emerson fittipaldi","james hunt","carlos reutemann","clay regazzoni","niki lauda","carlos pace","ronnie peterson","jody scheckter","patrick depailler","denny hulme"],
        "Gran Premio de Brasil": ["carlos pace","emerson fittipaldi","jochen mass","clay regazzoni","carlos reutemann","niki lauda","ronnie peterson","james hunt","jody scheckter","patrick depailler"],
        "Gran Premio de Sudáfrica": ["jody scheckter","carlos reutemann","patrick depailler","niki lauda","jochen mass","james hunt","clay regazzoni","emerson fittipaldi","ronnie peterson","carlos pace"],
        "Gran Premio de España": ["jochen mass","jacky ickx","carlos reutemann","niki lauda","emerson fittipaldi","clay regazzoni","jody scheckter","james hunt","ronnie peterson","patrick depailler"],
        "Gran Premio de Mónaco": ["niki lauda","emerson fittipaldi","carlos pace","jochen mass","patrick depailler","clay regazzoni","jody scheckter","carlos reutemann","james hunt","ronnie peterson"],
        "Gran Premio de Bélgica": ["niki lauda","jody scheckter","carlos reutemann","clay regazzoni","emerson fittipaldi","jochen mass","carlos pace","james hunt","ronnie peterson","patrick depailler"],
        "Gran Premio de Suecia": ["niki lauda","carlos reutemann","clay regazzoni","jochen mass","emerson fittipaldi","ronnie peterson","jody scheckter","james hunt","carlos pace","patrick depailler"],
        "Gran Premio de Países Bajos": ["james hunt","niki lauda","clay regazzoni","carlos reutemann","ronnie peterson","carlos pace","jody scheckter","jochen mass","emerson fittipaldi","patrick depailler"],
        "Gran Premio de Francia": ["niki lauda","james hunt","jochen mass","emerson fittipaldi","clay regazzoni","carlos reutemann","jody scheckter","carlos pace","ronnie peterson","patrick depailler"],
        "Gran Premio de Gran Bretaña": ["emerson fittipaldi","carlos pace","jochen mass","niki lauda","carlos reutemann","jody scheckter","james hunt","clay regazzoni","ronnie peterson","patrick depailler"],
        "Gran Premio de Alemania": ["carlos reutemann","clay regazzoni","jacques laffite","jochen mass","emerson fittipaldi","jody scheckter","niki lauda","ronnie peterson","james hunt","patrick depailler"],
        "Gran Premio de Austria": ["vittorio brambilla","james hunt","jochen mass","carlos reutemann","niki lauda","clay regazzoni","emerson fittipaldi","jody scheckter","carlos pace","ronnie peterson"],
        "Gran Premio de Italia": ["clay regazzoni","emerson fittipaldi","niki lauda","carlos reutemann","james hunt","jochen mass","jody scheckter","carlos pace","ronnie peterson","patrick depailler"],
        "Gran Premio de Estados Unidos": ["niki lauda","emerson fittipaldi","jochen mass","carlos reutemann","jody scheckter","clay regazzoni","james hunt","carlos pace","ronnie peterson","patrick depailler"],
    },
    1976: {
        "Gran Premio de Brasil": ["niki lauda","patrick depailler","tom pryce","jody scheckter","emerson fittipaldi","jochen mass","james hunt","clay regazzoni","carlos pace","ronnie peterson"],
        "Gran Premio de Sudáfrica": ["niki lauda","james hunt","jochen mass","jody scheckter","clay regazzoni","emerson fittipaldi","carlos pace","ronnie peterson","patrick depailler","mario andretti"],
        "Gran Premio de Estados Unidos Oeste": ["clay regazzoni","niki lauda","patrick depailler","james hunt","jochen mass","jody scheckter","emerson fittipaldi","carlos pace","ronnie peterson","mario andretti"],
        "Gran Premio de España": ["james hunt","niki lauda","gunnar nilsson","carlos reutemann","clay regazzoni","jody scheckter","emerson fittipaldi","jochen mass","ronnie peterson","patrick depailler"],
        "Gran Premio de Bélgica": ["niki lauda","clay regazzoni","jochen mass","jody scheckter","james hunt","carlos reutemann","emerson fittipaldi","ronnie peterson","patrick depailler","mario andretti"],
        "Gran Premio de Mónaco": ["niki lauda","jody scheckter","patrick depailler","hans joachim stuck","jochen mass","emerson fittipaldi","carlos pace","clay regazzoni","ronnie peterson","james hunt"],
        "Gran Premio de Suecia": ["jody scheckter","niki lauda","patrick depailler","jochen mass","emerson fittipaldi","carlos reutemann","james hunt","clay regazzoni","ronnie peterson","mario andretti"],
        "Gran Premio de Francia": ["james hunt","patrick depailler","jochen mass","niki lauda","clay regazzoni","jody scheckter","emerson fittipaldi","carlos reutemann","ronnie peterson","carlos pace"],
        "Gran Premio de Gran Bretaña": ["james hunt","niki lauda","jochen mass","gunnar nilsson","jody scheckter","patrick depailler","clay regazzoni","emerson fittipaldi","carlos reutemann","ronnie peterson"],
        "Gran Premio de Alemania": ["james hunt","jochen mass","carlos reutemann","jody scheckter","gunnar nilsson","niki lauda","clay regazzoni","emerson fittipaldi","ronnie peterson","patrick depailler"],
        "Gran Premio de Austria": ["john watson","james hunt","gunnar nilsson","ronnie peterson","jody scheckter","niki lauda","jochen mass","carlos reutemann","clay regazzoni","emerson fittipaldi"],
        "Gran Premio de Países Bajos": ["james hunt","clay regazzoni","niki lauda","ronnie peterson","jody scheckter","gunnar nilsson","jochen mass","carlos reutemann","emerson fittipaldi","patrick depailler"],
        "Gran Premio de Italia": ["ronnie peterson","clay regazzoni","james hunt","niki lauda","jochen mass","jody scheckter","gunnar nilsson","carlos reutemann","emerson fittipaldi","patrick depailler"],
        "Gran Premio de Canadá": ["james hunt","patrick depailler","mario andretti","jochen mass","jody scheckter","gunnar nilsson","clay regazzoni","niki lauda","emerson fittipaldi","ronnie peterson"],
        "Gran Premio de Estados Unidos Este": ["james hunt","jochen mass","niki lauda","ronnie peterson","jody scheckter","gunnar nilsson","carlos reutemann","clay regazzoni","emerson fittipaldi","patrick depailler"],
        "Gran Premio de Japón": ["mario andretti","jody scheckter","james hunt","patrick depailler","jochen mass","gunnar nilsson","clay regazzoni","niki lauda","ronnie peterson","emerson fittipaldi"],
    },
    1977: {
        "Gran Premio de Argentina": ["jody scheckter","carlos pace","mario andretti","emerson fittipaldi","james hunt","jochen mass","niki lauda","patrick depailler","clay regazzoni","gunnar nilsson"],
        "Gran Premio de Brasil": ["carlos reutemann","james hunt","niki lauda","emerson fittipaldi","jochen mass","jody scheckter","mario andretti","gunnar nilsson","patrick depailler","clay regazzoni"],
        "Gran Premio de Sudáfrica": ["niki lauda","jody scheckter","patrick depailler","james hunt","jochen mass","john watson","emerson fittipaldi","mario andretti","clay regazzoni","gunnar nilsson"],
        "Gran Premio de Estados Unidos Oeste": ["mario andretti","niki lauda","james hunt","emerson fittipaldi","jody scheckter","patrick depailler","jochen mass","clay regazzoni","gunnar nilsson","carlos reutemann"],
        "Gran Premio de España": ["mario andretti","carlos reutemann","james hunt","jochen mass","jody scheckter","emerson fittipaldi","niki lauda","patrick depailler","clay regazzoni","gunnar nilsson"],
        "Gran Premio de Mónaco": ["jody scheckter","niki lauda","carlos reutemann","james hunt","jochen mass","mario andretti","emerson fittipaldi","patrick depailler","clay regazzoni","gunnar nilsson"],
        "Gran Premio de Bélgica": ["gunnar nilsson","niki lauda","ronnie peterson","jody scheckter","james hunt","jochen mass","emerson fittipaldi","mario andretti","carlos reutemann","patrick depailler"],
        "Gran Premio de Suecia": ["james hunt","niki lauda","gunnar nilsson","jochen mass","jody scheckter","emerson fittipaldi","mario andretti","carlos reutemann","patrick depailler","clay regazzoni"],
        "Gran Premio de Francia": ["mario andretti","john watson","james hunt","niki lauda","ronnie peterson","jochen mass","gunnar nilsson","jody scheckter","emerson fittipaldi","carlos reutemann"],
        "Gran Premio de Gran Bretaña": ["james hunt","niki lauda","gunnar nilsson","jochen mass","jody scheckter","mario andretti","emerson fittipaldi","carlos reutemann","ronnie peterson","patrick depailler"],
        "Gran Premio de Alemania": ["niki lauda","jody scheckter","hans joachim stuck","jochen mass","gunnar nilsson","james hunt","emerson fittipaldi","mario andretti","carlos reutemann","patrick depailler"],
        "Gran Premio de Austria": ["alan jones","niki lauda","gunnar nilsson","jochen mass","jody scheckter","james hunt","emerson fittipaldi","mario andretti","carlos reutemann","ronnie peterson"],
        "Gran Premio de Países Bajos": ["niki lauda","jody scheckter","gunnar nilsson","jochen mass","james hunt","emerson fittipaldi","mario andretti","carlos reutemann","ronnie peterson","patrick depailler"],
        "Gran Premio de Italia": ["mario andretti","niki lauda","jody scheckter","jochen mass","gunnar nilsson","james hunt","emerson fittipaldi","carlos reutemann","ronnie peterson","clay regazzoni"],
        "Gran Premio de Estados Unidos Este": ["james hunt","mario andretti","niki lauda","jochen mass","jody scheckter","gunnar nilsson","emerson fittipaldi","carlos reutemann","ronnie peterson","clay regazzoni"],
        "Gran Premio de Canadá": ["jody scheckter","patrick depailler","jochen mass","niki lauda","mario andretti","james hunt","gunnar nilsson","emerson fittipaldi","carlos reutemann","ronnie peterson"],
        "Gran Premio de Japón": ["james hunt","carlos reutemann","mario andretti","jody scheckter","niki lauda","jochen mass","gunnar nilsson","emerson fittipaldi","ronnie peterson","patrick depailler"],
    },
    1978: {
        "Gran Premio de Argentina": ["mario andretti","niki lauda","patrick depailler","james hunt","ronnie peterson","jody scheckter","emerson fittipaldi","carlos reutemann","jochen mass","alan jones"],
        "Gran Premio de Brasil": ["carlos reutemann","emerson fittipaldi","mario andretti","jody scheckter","niki lauda","ronnie peterson","james hunt","patrick depailler","jochen mass","alan jones"],
        "Gran Premio de Sudáfrica": ["ronnie peterson","mario andretti","niki lauda","emerson fittipaldi","jody scheckter","carlos reutemann","james hunt","patrick depailler","jochen mass","alan jones"],
        "Gran Premio de Estados Unidos Oeste": ["carlos reutemann","mario andretti","niki lauda","jody scheckter","emerson fittipaldi","ronnie peterson","james hunt","patrick depailler","jochen mass","alan jones"],
        "Gran Premio de Mónaco": ["patrick depailler","niki lauda","jody scheckter","carlos reutemann","emerson fittipaldi","mario andretti","ronnie peterson","james hunt","jochen mass","alan jones"],
        "Gran Premio de Bélgica": ["mario andretti","ronnie peterson","carlos reutemann","niki lauda","emerson fittipaldi","jody scheckter","james hunt","patrick depailler","jochen mass","alan jones"],
        "Gran Premio de España": ["mario andretti","ronnie peterson","niki lauda","jody scheckter","emerson fittipaldi","carlos reutemann","james hunt","patrick depailler","jochen mass","alan jones"],
        "Gran Premio de Suecia": ["niki lauda","riccardo patrese","ronnie peterson","mario andretti","jody scheckter","emerson fittipaldi","carlos reutemann","james hunt","patrick depailler","jochen mass"],
        "Gran Premio de Francia": ["mario andretti","ronnie peterson","james hunt","jody scheckter","niki lauda","emerson fittipaldi","carlos reutemann","patrick depailler","jochen mass","alan jones"],
        "Gran Premio de Gran Bretaña": ["carlos reutemann","niki lauda","jody scheckter","mario andretti","ronnie peterson","james hunt","emerson fittipaldi","patrick depailler","jochen mass","alan jones"],
        "Gran Premio de Alemania": ["mario andretti","jody scheckter","niki lauda","emerson fittipaldi","ronnie peterson","carlos reutemann","james hunt","patrick depailler","jochen mass","alan jones"],
        "Gran Premio de Austria": ["ronnie peterson","patrick depailler","niki lauda","mario andretti","emerson fittipaldi","jody scheckter","carlos reutemann","james hunt","jochen mass","alan jones"],
        "Gran Premio de Países Bajos": ["mario andretti","ronnie peterson","niki lauda","emerson fittipaldi","jody scheckter","carlos reutemann","james hunt","patrick depailler","jochen mass","alan jones"],
        "Gran Premio de Italia": ["niki lauda","carlos reutemann","jody scheckter","james hunt","emerson fittipaldi","mario andretti","patrick depailler","jochen mass","alan jones","riccardo patrese"],
        "Gran Premio de Estados Unidos Este": ["carlos reutemann","mario andretti","niki lauda","jody scheckter","james hunt","emerson fittipaldi","ronnie peterson","patrick depailler","jochen mass","alan jones"],
        "Gran Premio de Canadá": ["jody scheckter","mario andretti","niki lauda","emerson fittipaldi","carlos reutemann","james hunt","ronnie peterson","patrick depailler","jochen mass","alan jones"],
    },
    1979: {
        "Gran Premio de Argentina": ["jacques laffite","carlos reutemann","jody scheckter","patrick depailler","mario andretti","gilles villeneuve","niki lauda","carlos pace","alan jones","jochen mass"],
        "Gran Premio de Brasil": ["jacques laffite","patrick depailler","mario andretti","jody scheckter","gilles villeneuve","carlos reutemann","niki lauda","alan jones","jochen mass","carlos pace"],
        "Gran Premio de Sudáfrica": ["gilles villeneuve","jody scheckter","jean pierre jarier","carlos reutemann","mario andretti","jochen mass","niki lauda","alan jones","patrick depailler","carlos pace"],
        "Gran Premio de Estados Unidos Oeste": ["gilles villeneuve","jody scheckter","carlos reutemann","mario andretti","jean pierre jarier","niki lauda","jochen mass","alan jones","patrick depailler","carlos pace"],
        "Gran Premio de España": ["patrick depailler","carlos reutemann","mario andretti","jody scheckter","gilles villeneuve","niki lauda","jochen mass","alan jones","jean pierre jarier","carlos pace"],
        "Gran Premio de Bélgica": ["jody scheckter","gilles villeneuve","alan jones","carlos reutemann","mario andretti","niki lauda","jean pierre jarier","jochen mass","patrick depailler","carlos pace"],
        "Gran Premio de Mónaco": ["jody scheckter","clay regazzoni","carlos reutemann","john watson","patrick depailler","mario andretti","gilles villeneuve","niki lauda","jochen mass","alan jones"],
        "Gran Premio de Francia": ["jean pierre jabouille","gilles villeneuve","alan jones","jody scheckter","clay regazzoni","carlos reutemann","mario andretti","niki lauda","jochen mass","patrick depailler"],
        "Gran Premio de Gran Bretaña": ["clay regazzoni","alan jones","jody scheckter","gilles villeneuve","carlos reutemann","mario andretti","niki lauda","jochen mass","jean pierre jarier","patrick depailler"],
        "Gran Premio de Alemania": ["alan jones","clay regazzoni","jacky ickx","jody scheckter","gilles villeneuve","carlos reutemann","mario andretti","niki lauda","jochen mass","jean pierre jarier"],
        "Gran Premio de Austria": ["alan jones","gilles villeneuve","jody scheckter","clay regazzoni","carlos reutemann","mario andretti","niki lauda","jochen mass","jean pierre jarier","patrick depailler"],
        "Gran Premio de Países Bajos": ["alan jones","jody scheckter","gilles villeneuve","carlos reutemann","mario andretti","niki lauda","clay regazzoni","jochen mass","jean pierre jarier","patrick depailler"],
        "Gran Premio de Italia": ["jody scheckter","gilles villeneuve","clay regazzoni","alan jones","carlos reutemann","mario andretti","niki lauda","jochen mass","jean pierre jarier","patrick depailler"],
        "Gran Premio de Canadá": ["alan jones","gilles villeneuve","clay regazzoni","jody scheckter","carlos reutemann","mario andretti","niki lauda","jochen mass","jean pierre jarier","patrick depailler"],
        "Gran Premio de Estados Unidos Este": ["gilles villeneuve","jody scheckter","alan jones","clay regazzoni","carlos reutemann","mario andretti","niki lauda","jochen mass","jean pierre jarier","patrick depailler"],
    },
    1980: {
        "Gran Premio de Argentina": ["alan jones","nelson piquet","keke rosberg","elio de angelis","carlos reutemann","gilles villeneuve","didier pironi","jody scheckter","jochen mass","jean pierre jabouille"],
        "Gran Premio de Brasil": ["rene arnoux","elio de angelis","alan jones","carlos reutemann","didier pironi","jean pierre jabouille","nelson piquet","gilles villeneuve","jochen mass","jody scheckter"],
        "Gran Premio de Sudáfrica": ["rene arnoux","alan jones","carlos reutemann","didier pironi","nelson piquet","gilles villeneuve","jochen mass","jody scheckter","jean pierre jabouille","elio de angelis"],
        "Gran Premio de Estados Unidos Oeste": ["nelson piquet","riccardo patrese","gilles villeneuve","alan jones","carlos reutemann","didier pironi","jochen mass","jody scheckter","rene arnoux","elio de angelis"],
        "Gran Premio de Bélgica": ["didier pironi","alan jones","carlos reutemann","nelson piquet","gilles villeneuve","jochen mass","jody scheckter","rene arnoux","elio de angelis","jean pierre jabouille"],
        "Gran Premio de Mónaco": ["carlos reutemann","jody scheckter","nelson piquet","gilles villeneuve","jean pierre jabouille","alan jones","didier pironi","jochen mass","rene arnoux","elio de angelis"],
        "Gran Premio de Francia": ["alan jones","didier pironi","carlos reutemann","nelson piquet","gilles villeneuve","jochen mass","jody scheckter","rene arnoux","jean pierre jabouille","elio de angelis"],
        "Gran Premio de Gran Bretaña": ["alan jones","carlos reutemann","nelson piquet","didier pironi","gilles villeneuve","jochen mass","jody scheckter","rene arnoux","jean pierre jabouille","elio de angelis"],
        "Gran Premio de Alemania": ["alan jones","carlos reutemann","nelson piquet","didier pironi","jochen mass","gilles villeneuve","jody scheckter","rene arnoux","jean pierre jabouille","elio de angelis"],
        "Gran Premio de Austria": ["jean pierre jabouille","carlos reutemann","alan jones","nelson piquet","didier pironi","gilles villeneuve","jochen mass","jody scheckter","rene arnoux","elio de angelis"],
        "Gran Premio de Países Bajos": ["nelson piquet","rene arnoux","alan jones","carlos reutemann","gilles villeneuve","didier pironi","jochen mass","jody scheckter","jean pierre jabouille","elio de angelis"],
        "Gran Premio de Italia": ["nelson piquet","alan jones","carlos reutemann","didier pironi","gilles villeneuve","jochen mass","jody scheckter","rene arnoux","jean pierre jabouille","elio de angelis"],
        "Gran Premio de Canadá": ["alan jones","carlos reutemann","gilles villeneuve","didier pironi","jody scheckter","nelson piquet","jochen mass","rene arnoux","jean pierre jabouille","elio de angelis"],
        "Gran Premio de Estados Unidos Este": ["alan jones","carlos reutemann","nelson piquet","gilles villeneuve","didier pironi","jochen mass","jody scheckter","rene arnoux","jean pierre jabouille","elio de angelis"],
    },
    1981: {
        "Gran Premio de Estados Unidos Oeste": ["alan jones","carlos reutemann","nelson piquet","riccardo patrese","john watson","gilles villeneuve","elio de angelis","eddie cheever","patrick tambay","marc surer"],
        "Gran Premio de Brasil": ["carlos reutemann","alan jones","riccardo patrese","marc surer","elio de angelis","hector rebaque","john watson","keke rosberg","derek daly","nelson piquet"],
        "Gran Premio de Argentina": ["nelson piquet","carlos reutemann","alain prost","alan jones","riccardo patrese","hector rebaque","elio de angelis","keke rosberg","marc surer","derek daly"],
        "Gran Premio de San Marino": ["nelson piquet","riccardo patrese","carlos reutemann","hector rebaque","gilles villeneuve","derek daly","elio de angelis","didier pironi","marc surer","john watson"],
        "Gran Premio de Bélgica": ["carlos reutemann","nigel mansell","riccardo patrese","gilles villeneuve","elio de angelis","john watson","alan jones","hector rebaque","derek daly","marc surer"],
        "Gran Premio de Mónaco": ["gilles villeneuve","alan jones","john watson","carlos reutemann","derek daly","didier pironi","marc surer","elio de angelis","riccardo patrese","hector rebaque"],
        "Gran Premio de España": ["gilles villeneuve","john watson","carlos reutemann","alan jones","elio de angelis","keke rosberg","hector rebaque","marc surer","riccardo patrese","nigel mansell"],
        "Gran Premio de Francia": ["alain prost","john watson","nelson piquet","riccardo patrese","alan jones","keke rosberg","elio de angelis","gilles villeneuve","carlos reutemann","hector rebaque"],
        "Gran Premio de Gran Bretaña": ["john watson","carlos reutemann","alan jones","keke rosberg","hector rebaque","elio de angelis","riccardo patrese","derek daly","marc surer","nigel mansell"],
        "Gran Premio de Alemania": ["nelson piquet","alain prost","john watson","carlos reutemann","hector rebaque","derek daly","riccardo patrese","elio de angelis","marc surer","keke rosberg"],
        "Gran Premio de Austria": ["jacques laffite","carlos reutemann","nelson piquet","alan jones","john watson","elio de angelis","alain prost","hector rebaque","gilles villeneuve","riccardo patrese"],
        "Gran Premio de Países Bajos": ["alain prost","nelson piquet","alan jones","hector rebaque","elio de angelis","riccardo patrese","carlos reutemann","john watson","eddie cheever","marc surer"],
        "Gran Premio de Italia": ["alain prost","alan jones","carlos reutemann","nelson piquet","riccardo patrese","hector rebaque","john watson","elio de angelis","eddie cheever","marc surer"],
        "Gran Premio de Canadá": ["jacques laffite","john watson","gilles villeneuve","elio de angelis","nelson piquet","carlos reutemann","keke rosberg","hector rebaque","marc surer","riccardo patrese"],
        "Gran Premio de Las Vegas": ["alan jones","alain prost","bruno giacomelli","nelson piquet","carlos reutemann","riccardo patrese","elio de angelis","keke rosberg","john watson","hector rebaque"],
    },
    1982: {
        "Gran Premio de Sudáfrica": ["alain prost","carlos reutemann","rene arnoux","riccardo patrese","niki lauda","keke rosberg","elio de angelis","gilles villeneuve","didier pironi","john watson"],
        "Gran Premio de Brasil": ["alain prost","john watson","nelson piquet","carlos reutemann","niki lauda","keke rosberg","elio de angelis","riccardo patrese","derek daly","eddie cheever"],
        "Gran Premio de Estados Unidos Oeste": ["niki lauda","keke rosberg","riccardo patrese","elio de angelis","andrea de cesaris","gilles villeneuve","john watson","carlos reutemann","derek daly","nelson piquet"],
        "Gran Premio de San Marino": ["didier pironi","gilles villeneuve","michele alboreto","jean pierre jarier","riccardo patrese","nelson piquet","marc surer","elio de angelis","derek daly","teo fabi"],
        "Gran Premio de Bélgica": ["john watson","keke rosberg","eddie cheever","elio de angelis","derek daly","carlos reutemann","niki lauda","nigel mansell","riccardo patrese","andrea de cesaris"],
        "Gran Premio de Mónaco": ["riccardo patrese","didier pironi","andrea de cesaris","nigel mansell","elio de angelis","derek daly","rene arnoux","marc surer","keke rosberg","alain prost"],
        "Gran Premio de Detroit": ["john watson","eddie cheever","didier pironi","keke rosberg","riccardo patrese","elio de angelis","niki lauda","andrea de cesaris","nigel mansell","carlos reutemann"],
        "Gran Premio de Canadá": ["nelson piquet","riccardo patrese","john watson","elio de angelis","carlos reutemann","keke rosberg","alain prost","marc surer","andrea de cesaris","nigel mansell"],
        "Gran Premio de Países Bajos": ["didier pironi","nelson piquet","keke rosberg","john watson","riccardo patrese","elio de angelis","andrea de cesaris","alain prost","niki lauda","carlos reutemann"],
        "Gran Premio de Gran Bretaña": ["niki lauda","didier pironi","patrick tambay","elio de angelis","derek daly","keke rosberg","alain prost","marc surer","carlos reutemann","eddie cheever"],
        "Gran Premio de Francia": ["rene arnoux","alain prost","didier pironi","riccardo patrese","keke rosberg","john watson","elio de angelis","derek daly","marc surer","niki lauda"],
        "Gran Premio de Alemania": ["patrick tambay","eddie cheever","riccardo patrese","keke rosberg","john watson","alain prost","nelson piquet","elio de angelis","nigel mansell","derek daly"],
        "Gran Premio de Austria": ["elio de angelis","keke rosberg","alain prost","riccardo patrese","niki lauda","john watson","nelson piquet","derek daly","marc surer","andrea de cesaris"],
        "Gran Premio de Suiza": ["keke rosberg","alain prost","niki lauda","nelson piquet","riccardo patrese","john watson","elio de angelis","derek daly","marc surer","andrea de cesaris"],
        "Gran Premio de Italia": ["rene arnoux","patrick tambay","mario andretti","keke rosberg","niki lauda","elio de angelis","john watson","riccardo patrese","derek daly","nelson piquet"],
        "Gran Premio de Las Vegas": ["michelle alboreto","john watson","eddie cheever","alain prost","keke rosberg","chico serra","riccardo patrese","derek daly","elio de angelis","marc surer"],
    },
    1983: {
        "Gran Premio de Brasil": ["nelson piquet","keke rosberg","alain prost","niki lauda","john watson","elio de angelis","eddie cheever","patrick tambay","jaques laffite","marc surer"],
        "Gran Premio de Estados Unidos Oeste": ["john watson","niki lauda","rene arnoux","keke rosberg","jaques laffite","marc surer","patrick tambay","david thaddeus","elio de angelis","riccardo patrese"],
        "Gran Premio de Francia": ["alain prost","nelson piquet","eddie cheever","derek warwick","keke rosberg","john watson","patrick tambay","elio de angelis","marc surer","riccardo patrese"],
        "Gran Premio de San Marino": ["patrick tambay","riccardo patrese","alain prost","keke rosberg","nelson piquet","john watson","elio de angelis","marc surer","jaques laffite","nigel mansell"],
        "Gran Premio de Mónaco": ["keke rosberg","nelson piquet","alain prost","elio de angelis","john watson","jaques laffite","patrick tambay","riccardo patrese","marc surer","derek warwick"],
        "Gran Premio de Bélgica": ["alain prost","nelson piquet","eddie cheever","keke rosberg","riccardo patrese","nigel mansell","elio de angelis","derek warwick","marc surer","john watson"],
        "Gran Premio de Detroit": ["nelson piquet","john watson","rene arnoux","keke rosberg","eddie cheever","elio de angelis","alain prost","marc surer","derek warwick","riccardo patrese"],
        "Gran Premio de Canadá": ["rene arnoux","eddie cheever","nelson piquet","keke rosberg","john watson","alain prost","nigel mansell","elio de angelis","derek warwick","marc surer"],
        "Gran Premio de Gran Bretaña": ["alain prost","nelson piquet","john watson","jaques laffite","riccardo patrese","keke rosberg","elio de angelis","derek warwick","marc surer","nigel mansell"],
        "Gran Premio de Alemania": ["rene arnoux","andrea de cesaris","riccardo patrese","keke rosberg","alain prost","derek warwick","elio de angelis","nigel mansell","john watson","marc surer"],
        "Gran Premio de Austria": ["alain prost","nelson piquet","rene arnoux","riccardo patrese","keke rosberg","elio de angelis","derek warwick","marc surer","nigel mansell","john watson"],
        "Gran Premio de Países Bajos": ["rene arnoux","john watson","eddie cheever","keke rosberg","alain prost","riccardo patrese","elio de angelis","nelson piquet","nigel mansell","derek warwick"],
        "Gran Premio de Italia": ["nelson piquet","rene arnoux","eddie cheever","riccardo patrese","alain prost","keke rosberg","elio de angelis","marc surer","derek warwick","nigel mansell"],
        "Gran Premio de Europa": ["alain prost","nelson piquet","rene arnoux","elio de angelis","derek warwick","john watson","riccardo patrese","nigel mansell","jaques laffite","marc surer"],
        "Gran Premio de Sudáfrica": ["riccardo patrese","andrea de cesaris","nelson piquet","keke rosberg","alain prost","elio de angelis","rene arnoux","derek warwick","marc surer","john watson"],
    },
    1984: {
        "Gran Premio de Brasil": ["alain prost","keke rosberg","elio de angelis","derek warwick","rene arnoux","eddie cheever","nigel mansell","marc surer","riccardo patrese","martin brundle"],
        "Gran Premio de Sudáfrica": ["niki lauda","alain prost","riccardo patrese","derek warwick","elio de angelis","rene arnoux","marc surer","keke rosberg","nigel mansell","johnny cecotto"],
        "Gran Premio de Bélgica": ["michelle alboreto","derek warwick","rene arnoux","keke rosberg","nigel mansell","elio de angelis","riccardo patrese","alain prost","marc surer","teo fabi"],
        "Gran Premio de San Marino": ["alain prost","rene arnoux","elio de angelis","derek warwick","keke rosberg","riccardo patrese","nigel mansell","marc surer","teo fabi","andrea de cesaris"],
        "Gran Premio de Francia": ["niki lauda","alain prost","rene arnoux","keke rosberg","elio de angelis","derek warwick","marc surer","nigel mansell","riccardo patrese","andrea de cesaris"],
        "Gran Premio de Mónaco": ["alain prost","ayrton senna","stefan bellof","rene arnoux","keke rosberg","michelle alboreto","nigel mansell","niki lauda","derek bell","jonathan palmer"],
        "Gran Premio de Canadá": ["nelson piquet","alain prost","elio de angelis","niki lauda","keke rosberg","rene arnoux","riccardo patrese","derek warwick","marc surer","johnny cecotto"],
        "Gran Premio de Detroit": ["nelson piquet","alain prost","keke rosberg","derek warwick","elio de angelis","rene arnoux","teo fabi","marc surer","nigel mansell","riccardo patrese"],
        "Gran Premio de Dallas": ["keke rosberg","rene arnoux","elio de angelis","derek warwick","niki lauda","alain prost","michelle alboreto","marc surer","riccardo patrese","teo fabi"],
        "Gran Premio de Gran Bretaña": ["niki lauda","derek warwick","ayrton senna","elio de angelis","jonathan palmer","nigel mansell","alain prost","jacques laffite","niki lauda","martin brundle"],
        "Gran Premio de Alemania": ["alain prost","niki lauda","derek warwick","rene arnoux","keke rosberg","elio de angelis","riccardo patrese","marc surer","teo fabi","andrea de cesaris"],
        "Gran Premio de Austria": ["niki lauda","alain prost","nelson piquet","riccardo patrese","elio de angelis","rene arnoux","keke rosberg","derek warwick","marc surer","nigel mansell"],
        "Gran Premio de Países Bajos": ["alain prost","niki lauda","nigel mansell","elio de angelis","derek warwick","rene arnoux","keke rosberg","riccardo patrese","marc surer","jonathan palmer"],
        "Gran Premio de Italia": ["niki lauda","michelle alboreto","riccardo patrese","stefan johansson","elio de angelis","keke rosberg","marc surer","derek warwick","rene arnoux","nigel mansell"],
        "Gran Premio de Europa": ["alain prost","michelle alboreto","niki lauda","elio de angelis","keke rosberg","riccardo patrese","derek warwick","marc surer","teo fabi","nigel mansell"],
        "Gran Premio de Portugal": ["alain prost","niki lauda","ayrton senna","michelle alboreto","elio de angelis","keke rosberg","riccardo patrese","derek warwick","rene arnoux","nigel mansell"],
    },
    1985: {
        "Gran Premio de Brasil": ["alain prost","michelle alboreto","elio de angelis","keke rosberg","ayrton senna","nigel mansell","stefan johansson","derek warwick","riccardo patrese","thierry boutsen"],
        "Gran Premio de Portugal": ["ayrton senna","alain prost","michelle alboreto","riccardo patrese","elio de angelis","nigel mansell","derek warwick","stefan johansson","keke rosberg","marc surer"],
        "Gran Premio de San Marino": ["elio de angelis","thierry boutsen","patrick tambay","ayrton senna","stefan johansson","riccardo patrese","marc surer","derek warwick","michelle alboreto","keke rosberg"],
        "Gran Premio de Mónaco": ["ayrton senna","michelle alboreto","alain prost","elio de angelis","keke rosberg","derek warwick","riccardo patrese","nigel mansell","stefan johansson","marc surer"],
        "Gran Premio de Canadá": ["michelle alboreto","stefan johansson","alain prost","ayrton senna","keke rosberg","riccardo patrese","elio de angelis","thierry boutsen","patrick tambay","marc surer"],
        "Gran Premio de Detroit": ["keke rosberg","ayrton senna","stefan johansson","michelle alboreto","elio de angelis","nigel mansell","alain prost","thierry boutsen","derek warwick","riccardo patrese"],
        "Gran Premio de Francia": ["nigel mansell","alain prost","elio de angelis","keke rosberg","ayrton senna","michelle alboreto","riccardo patrese","derek warwick","stefan johansson","thierry boutsen"],
        "Gran Premio de Gran Bretaña": ["alain prost","michelle alboreto","nigel mansell","ayrton senna","keke rosberg","riccardo patrese","elio de angelis","derek warwick","thierry boutsen","stefan johansson"],
        "Gran Premio de Alemania": ["michelle alboreto","alain prost","nigel mansell","ayrton senna","elio de angelis","stefan johansson","keke rosberg","derek warwick","riccardo patrese","thierry boutsen"],
        "Gran Premio de Austria": ["alain prost","ayrton senna","michelle alboreto","nigel mansell","elio de angelis","stefan johansson","keke rosberg","riccardo patrese","derek warwick","thierry boutsen"],
        "Gran Premio de Países Bajos": ["niki lauda","alain prost","ayrton senna","michelle alboreto","elio de angelis","nigel mansell","keke rosberg","stefan johansson","riccardo patrese","derek warwick"],
        "Gran Premio de Italia": ["ayrton senna","alain prost","elio de angelis","keke rosberg","riccardo patrese","nigel mansell","stefan johansson","derek warwick","thierry boutsen","michelle alboreto"],
        "Gran Premio de Bélgica": ["ayrton senna","nigel mansell","alain prost","michelle alboreto","elio de angelis","keke rosberg","riccardo patrese","derek warwick","stefan johansson","thierry boutsen"],
        "Gran Premio de Europa": ["nigel mansell","ayrton senna","alain prost","michelle alboreto","elio de angelis","keke rosberg","riccardo patrese","derek warwick","stefan johansson","thierry boutsen"],
        "Gran Premio de Sudáfrica": ["nigel mansell","keke rosberg","alain prost","michelle alboreto","ayrton senna","elio de angelis","riccardo patrese","derek warwick","stefan johansson","thierry boutsen"],
        "Gran Premio de Australia": ["keke rosberg","nigel mansell","ayrton senna","alain prost","michelle alboreto","elio de angelis","riccardo patrese","derek warwick","stefan johansson","thierry boutsen"],
    },
    1986: {
        "Gran Premio de Brasil": ["nelson piquet","ayrton senna","alain prost","keke rosberg","michelle alboreto","riccardo patrese","nigel mansell","rene arnoux","derek warwick","thierry boutsen"],
        "Gran Premio de España": ["ayrton senna","nigel mansell","alain prost","keke rosberg","nelson piquet","michelle alboreto","riccardo patrese","rene arnoux","derek warwick","thierry boutsen"],
        "Gran Premio de San Marino": ["alain prost","nelson piquet","gerhard berger","stefan johansson","riccardo patrese","andrea de cesaris","derek warwick","christian danner","jonathan palmer","thierry boutsen"],
        "Gran Premio de Mónaco": ["alain prost","keke rosberg","ayrton senna","nigel mansell","stefan johansson","michelle alboreto","riccardo patrese","rene arnoux","derek warwick","thierry boutsen"],
        "Gran Premio de Bélgica": ["nigel mansell","ayrton senna","stefan johansson","alain prost","keke rosberg","michelle alboreto","riccardo patrese","rene arnoux","derek warwick","thierry boutsen"],
        "Gran Premio de Canadá": ["nigel mansell","alain prost","nelson piquet","rene arnoux","keke rosberg","stefan johansson","michelle alboreto","riccardo patrese","derek warwick","thierry boutsen"],
        "Gran Premio de Detroit": ["ayrton senna","keke rosberg","alain prost","nigel mansell","nelson piquet","stefan johansson","derek warwick","michelle alboreto","riccardo patrese","thierry boutsen"],
        "Gran Premio de Francia": ["nigel mansell","alain prost","nelson piquet","keke rosberg","ayrton senna","stefan johansson","michelle alboreto","rene arnoux","derek warwick","thierry boutsen"],
        "Gran Premio de Gran Bretaña": ["nigel mansell","nelson piquet","alain prost","ayrton senna","keke rosberg","stefan johansson","michelle alboreto","riccardo patrese","derek warwick","thierry boutsen"],
        "Gran Premio de Alemania": ["nelson piquet","ayrton senna","nigel mansell","alain prost","keke rosberg","stefan johansson","michelle alboreto","riccardo patrese","derek warwick","rene arnoux"],
        "Gran Premio de Hungría": ["nelson piquet","ayrton senna","nigel mansell","stefan johansson","alain prost","keke rosberg","michelle alboreto","riccardo patrese","derek warwick","thierry boutsen"],
        "Gran Premio de Austria": ["alain prost","michelle alboreto","stefan johansson","nigel mansell","ayrton senna","keke rosberg","nelson piquet","riccardo patrese","derek warwick","thierry boutsen"],
        "Gran Premio de Italia": ["nelson piquet","nigel mansell","stefan johansson","alain prost","keke rosberg","ayrton senna","riccardo patrese","michelle alboreto","derek warwick","thierry boutsen"],
        "Gran Premio de Portugal": ["nigel mansell","alain prost","nelson piquet","ayrton senna","keke rosberg","stefan johansson","michelle alboreto","riccardo patrese","derek warwick","thierry boutsen"],
        "Gran Premio de México": ["berger","alain prost","ayrton senna","nelson piquet","nigel mansell","stefan johansson","keke rosberg","riccardo patrese","derek warwick","thierry boutsen"],
        "Gran Premio de Australia": ["alain prost","nelson piquet","stefan johansson","martin brundle","philippe streiff","thierry boutsen","philippe alliot","christian danner","alan jones","gerhard berger"],
    },
    1987: {
        "Gran Premio de Brasil": ["alain prost","nelson piquet","stefan johansson","ayrton senna","gerhard berger","michele alboreto","thierry boutsen","riccardo patrese","derek warwick","eddie cheever"],
        "Gran Premio de San Marino": ["nigel mansell","ayrton senna","stefan johansson","teo fabi","eddie cheever","thierry boutsen","satoru nakajima","riccardo patrese","derek warwick","jonathan palmer"],
        "Gran Premio de Bélgica": ["alain prost","stefan johansson","andrea de cesaris","michel alboreto","thierry boutsen","satoru nakajima","riccardo patrese","derek warwick","nigel mansell","ayrton senna"],
        "Gran Premio de Mónaco": ["ayrton senna","nelson piquet","michelle alboreto","gerhard berger","stefan johansson","thierry boutsen","riccardo patrese","derek warwick","satoru nakajima","nigel mansell"],
        "Gran Premio de Detroit": ["ayrton senna","nelson piquet","alain prost","riccardo patrese","eddie cheever","thierry boutsen","derek warwick","stefan johansson","satoru nakajima","michelle alboreto"],
        "Gran Premio de Francia": ["nigel mansell","alain prost","ayrton senna","nelson piquet","riccardo patrese","stefan johansson","gerhard berger","thierry boutsen","derek warwick","satoru nakajima"],
        "Gran Premio de Gran Bretaña": ["nigel mansell","nelson piquet","ayrton senna","alain prost","riccardo patrese","derek warwick","thierry boutsen","satoru nakajima","stefan johansson","gerhard berger"],
        "Gran Premio de Alemania": ["nelson piquet","stefan johansson","ayrton senna","thierry boutsen","gerhard berger","alain prost","riccardo patrese","derek warwick","satoru nakajima","eddie cheever"],
        "Gran Premio de Hungría": ["nelson piquet","ayrton senna","alain prost","thierry boutsen","riccardo patrese","derek warwick","satoru nakajima","stefan johansson","gerhard berger","michelle alboreto"],
        "Gran Premio de Austria": ["nigel mansell","nelson piquet","teo fabi","ayrton senna","thierry boutsen","gerhard berger","riccardo patrese","derek warwick","satoru nakajima","alain prost"],
        "Gran Premio de Italia": ["ayrton senna","nelson piquet","nigel mansell","alain prost","stefan johansson","thierry boutsen","riccardo patrese","derek warwick","satoru nakajima","gerhard berger"],
        "Gran Premio de Portugal": ["alain prost","gerhard berger","nelson piquet","nigel mansell","stefan johansson","thierry boutsen","riccardo patrese","derek warwick","satoru nakajima","ayrton senna"],
        "Gran Premio de España": ["nigel mansell","alain prost","ayrton senna","gerhard berger","stefan johansson","thierry boutsen","riccardo patrese","derek warwick","satoru nakajima","michelle alboreto"],
        "Gran Premio de México": ["nigel mansell","nelson piquet","riccardo patrese","eddie cheever","ayrton senna","teo fabi","thierry boutsen","satoru nakajima","derek warwick","gerhard berger"],
        "Gran Premio de Japón": ["gerhard berger","ayrton senna","thierry boutsen","riccardo patrese","derek warwick","satoru nakajima","nigel mansell","nelson piquet","stefan johansson","alain prost"],
        "Gran Premio de Australia": ["gerhard berger","ayrton senna","thierry boutsen","michelle alboreto","riccardo patrese","derek warwick","satoru nakajima","nigel mansell","stefan johansson","alain prost"],
    },
    1988: {
        "Gran Premio de Brasil": ["alain prost","gerhard berger","nelson piquet","thierry boutsen","derek warwick","andrea de cesaris","riccardo patrese","martin brundle","jonathan palmer","nicola larini"],
        "Gran Premio de San Marino": ["ayrton senna","alain prost","nelson piquet","thierry boutsen","derek warwick","andrea de cesaris","riccardo patrese","satoru nakajima","martin brundle","nigel mansell"],
        "Gran Premio de Mónaco": ["ayrton senna","alain prost","gerhard berger","michele alboreto","thierry boutsen","derek warwick","bernd schneider","stefano modena","alex caffi","pierluigi martini"],
        "Gran Premio de México": ["alain prost","ayrton senna","gerhard berger","michelle alboreto","thierry boutsen","derek warwick","nelson piquet","riccardo patrese","andrea de cesaris","satoru nakajima"],
        "Gran Premio de Canadá": ["ayrton senna","alain prost","thierry boutsen","nelson piquet","riccardo patrese","gerhard berger","derek warwick","satoru nakajima","andrea de cesaris","martin brundle"],
        "Gran Premio de Detroit": ["ayrton senna","alain prost","thierry boutsen","andrea de cesaris","nelson piquet","riccardo patrese","derek warwick","satoru nakajima","gerhard berger","martin brundle"],
        "Gran Premio de Francia": ["alain prost","ayrton senna","thierry boutsen","gerhard berger","nelson piquet","riccardo patrese","derek warwick","andrea de cesaris","satoru nakajima","martin brundle"],
        "Gran Premio de Gran Bretaña": ["ayrton senna","nigel mansell","alain prost","martin brundle","gerhard berger","stefan johansson","nelson piquet","derek warwick","thierry boutsen","mauricio gugelmin"],
        "Gran Premio de Alemania": ["ayrton senna","alain prost","gerhard berger","thierry boutsen","nelson piquet","riccardo patrese","derek warwick","satoru nakajima","martin brundle","andrea de cesaris"],
        "Gran Premio de Hungría": ["ayrton senna","alain prost","thierry boutsen","gerhard berger","derek warwick","riccardo patrese","mauricio gugelmin","ivan capelli","pierluigi martini","nelson piquet"],
        "Gran Premio de Bélgica": ["ayrton senna","alain prost","gerhard berger","thierry boutsen","nelson piquet","riccardo patrese","derek warwick","satoru nakajima","martin brundle","andrea de cesaris"],
        "Gran Premio de Italia": ["gerhard berger","michele alboreto","eddie cheever","derek warwick","thierry boutsen","riccardo patrese","andrea de cesaris","pierluigi martini","jonathan palmer","alex caffi"],
        "Gran Premio de Portugal": ["alain prost","ivan capelli","thierry boutsen","derek warwick","nelson piquet","riccardo patrese","andrea de cesaris","satoru nakajima","martin brundle","jonathan palmer"],
        "Gran Premio de España": ["alain prost","nigel mansell","ayrton senna","allessandro nannini","thierry boutsen","derek warwick","riccardo patrese","satoru nakajima","andrea de cesaris","martin brundle"],
        "Gran Premio de Japón": ["ayrton senna","alain prost","thierry boutsen","gerhard berger","nelson piquet","riccardo patrese","derek warwick","satoru nakajima","martin brundle","andrea de cesaris"],
        "Gran Premio de Australia": ["alain prost","ayrton senna","nelson piquet","thierry boutsen","riccardo patrese","gerhard berger","derek warwick","satoru nakajima","martin brundle","andrea de cesaris"],
    },
    1989: {
        "Gran Premio de Brasil": ["nigel mansell","ayrton senna","rene arnoux","thierry boutsen","allessandro nannini","derek warwick","nelson piquet","riccardo patrese","andrea de cesaris","satoru nakajima"],
        "Gran Premio de San Marino": ["ayrton senna","alain prost","allessandro nannini","thierry boutsen","gerhard berger","nelson piquet","derek warwick","riccardo patrese","andrea de cesaris","satoru nakajima"],
        "Gran Premio de Mónaco": ["ayrton senna","alain prost","stefano modena","nigel mansell","eddie cheever","riccardo patrese","gerhard berger","nelson piquet","emanuele pirro","oscar larrauri"],
        "Gran Premio de México": ["ayrton senna","riccardo patrese","derek warwick","thierry boutsen","allessandro nannini","gerhard berger","nelson piquet","andrea de cesaris","satoru nakajima","martin brundle"],
        "Gran Premio de Estados Unidos": ["ayrton senna","alain prost","riccardo patrese","thierry boutsen","allessandro nannini","derek warwick","nelson piquet","andrea de cesaris","satoru nakajima","martin brundle"],
        "Gran Premio de Canadá": ["thierry boutsen","riccardo patrese","allessandro nannini","ayrton senna","alain prost","andrea de cesaris","nelson piquet","derek warwick","satoru nakajima","martin brundle"],
        "Gran Premio de Francia": ["alain prost","ayrton senna","riccardo patrese","thierry boutsen","allessandro nannini","derek warwick","nelson piquet","andrea de cesaris","satoru nakajima","martin brundle"],
        "Gran Premio de Gran Bretaña": ["alain prost","nigel mansell","ayrton senna","gerhard berger","nelson piquet","thierry boutsen","stefano modena","christian danner","derek warwick","pierluigi martini"],
        "Gran Premio de Alemania": ["ayrton senna","alain prost","riccardo patrese","thierry boutsen","allessandro nannini","gerhard berger","nelson piquet","andrea de cesaris","satoru nakajima","derek warwick"],
        "Gran Premio de Hungría": ["nigel mansell","ayrton senna","thierry boutsen","alain prost","riccardo patrese","allessandro nannini","gerhard berger","nelson piquet","andrea de cesaris","satoru nakajima"],
        "Gran Premio de Bélgica": ["ayrton senna","alain prost","allessandro nannini","thierry boutsen","riccardo patrese","gerhard berger","nelson piquet","andrea de cesaris","satoru nakajima","derek warwick"],
        "Gran Premio de Italia": ["alain prost","gerhard berger","thierry boutsen","allessandro nannini","riccardo patrese","nigel mansell","derek warwick","andrea de cesaris","satoru nakajima","martin brundle"],
        "Gran Premio de Portugal": ["gerhard berger","alain prost","joao camoes","thierry boutsen","allessandro nannini","riccardo patrese","nelson piquet","andrea de cesaris","satoru nakajima","derek warwick"],
        "Gran Premio de España": ["ayrton senna","gerhard berger","alain prost","riccardo patrese","jean alesi","thierry boutsen","allessandro nannini","derek warwick","andrea de cesaris","satoru nakajima"],
        "Gran Premio de Japón": ["allessandro nannini","riccardo patrese","thierry boutsen","nelson piquet","satoru nakajima","alain prost","gerhard berger","derek warwick","andrea de cesaris","martin brundle"],
        "Gran Premio de Australia": ["thierry boutsen","allessandro nannini","riccardo patrese","satoru nakajima","martin brundle","derek warwick","nigel mansell","andrea de cesaris","alain prost","gerhard berger"],
    },
    1990: {
        "Gran Premio de Estados Unidos": ["ayrton senna","jean alesi","thierry boutsen","allessandro nannini","gerhard berger","nelson piquet","riccardo patrese","aguri suzuki","derek warwick","eric bernard"],
        "Gran Premio de Brasil": ["alain prost","gerhard berger","ayrton senna","nigel mansell","thierry boutsen","riccardo patrese","jean alesi","allessandro nannini","nelson piquet","derek warwick"],
        "Gran Premio de San Marino": ["riccardo patrese","gerhard berger","ayrton senna","alain prost","nigel mansell","thierry boutsen","allessandro nannini","nelson piquet","jean alesi","derek warwick"],
        "Gran Premio de Mónaco": ["ayrton senna","jean alesi","gerhard berger","thierry boutsen","roberto moreno","aguri suzuki","derek warwick","eric bernard","stefan johansson","alex caffi"],
        "Gran Premio de Canadá": ["ayrton senna","nelson piquet","nigel mansell","gerhard berger","riccardo patrese","thierry boutsen","jean alesi","derek warwick","allessandro nannini","aguri suzuki"],
        "Gran Premio de México": ["alain prost","nigel mansell","gerhard berger","ayrton senna","allessandro nannini","thierry boutsen","riccardo patrese","jean alesi","nelson piquet","derek warwick"],
        "Gran Premio de Francia": ["alain prost","ivan capelli","ayrton senna","nigel mansell","jean alesi","thierry boutsen","gerhard berger","riccardo patrese","allessandro nannini","nelson piquet"],
        "Gran Premio de Gran Bretaña": ["alain prost","thierry boutsen","gerhard berger","ayrton senna","nigel mansell","jean alesi","riccardo patrese","allessandro nannini","nelson piquet","derek warwick"],
        "Gran Premio de Alemania": ["ayrton senna","alain prost","gerhard berger","nigel mansell","riccardo patrese","thierry boutsen","jean alesi","allessandro nannini","nelson piquet","derek warwick"],
        "Gran Premio de Hungría": ["thierry boutsen","ayrton senna","allessandro nannini","nigel mansell","riccardo patrese","gerhard berger","eric bernard","derek warwick","alain prost","nelson piquet"],
        "Gran Premio de Bélgica": ["ayrton senna","alain prost","gerhard berger","nigel mansell","aguri suzuki","thierry boutsen","riccardo patrese","allessandro nannini","derek warwick","jean alesi"],
        "Gran Premio de Italia": ["ayrton senna","alain prost","gerhard berger","nigel mansell","thierry boutsen","riccardo patrese","jean alesi","allessandro nannini","nelson piquet","derek warwick"],
        "Gran Premio de Portugal": ["nigel mansell","ayrton senna","alain prost","gerhard berger","thierry boutsen","riccardo patrese","jean alesi","allessandro nannini","nelson piquet","derek warwick"],
        "Gran Premio de España": ["alain prost","nigel mansell","ayrton senna","gerhard berger","thierry boutsen","riccardo patrese","jean alesi","allessandro nannini","nelson piquet","aguri suzuki"],
        "Gran Premio de Japón": ["nelson piquet","roberto moreno","aguri suzuki","thierry boutsen","nigel mansell","jean alesi","riccardo patrese","derek warwick","alain prost","stefano modena"],
        "Gran Premio de Australia": ["nelson piquet","alain prost","thierry boutsen","roberto moreno","aguri suzuki","jean alesi","riccardo patrese","derek warwick","allessandro nannini","gerhard berger"],
    },
    1991: {
        "Gran Premio de Estados Unidos":  ["ayrton senna","nelson piquet","jean alesi","mika hakkinen","andrea de cesaris","emanuele pirro","riccardo patrese","pierluigi martini","bertrand gachot","eric bernard"],
        "Gran Premio de Brasil":          ["ayrton senna","riccardo patrese","gerhard berger","alain prost","nigel mansell","nelson piquet","andrea de cesaris","roberto moreno","pierluigi martini","emanuele pirro"],
        "Gran Premio de San Marino":      ["ayrton senna","gerhard berger","j.j. lehto","riccardo patrese","martin brundle","jean alesi","pierluigi martini","bertrand gachot","roberto moreno","aguri suzuki"],
        "Gran Premio de Mónaco":          ["ayrton senna","nigel mansell","jean alesi","roberto moreno","stefano modena","bertrand gachot","j.j. lehto","eric bernard","pierluigi martini","emanuele pirro"],
        "Gran Premio de Canadá":          ["nigel mansell","nelson piquet","michael schumacher","jean alesi","andrea de cesaris","riccardo patrese","bertrand gachot","mika hakkinen","mark blundell","emanuele pirro"],
        "Gran Premio de México":          ["riccardo patrese","nigel mansell","ayrton senna","alain prost","nelson piquet","jean alesi","gerhard berger","mika hakkinen","andrea de cesaris","emanuele pirro"],
        "Gran Premio de Francia":         ["nigel mansell","alain prost","ayrton senna","gerhard berger","riccardo patrese","jean alesi","andrea de cesaris","mika hakkinen","thierry boutsen","pierluigi martini"],
        "Gran Premio de Gran Bretaña":    ["nigel mansell","gerhard berger","alain prost","ayrton senna","michael schumacher","bertrand gachot","roberto moreno","mark blundell","ivan capelli","j.j. lehto"],
        "Gran Premio de Alemania":        ["nigel mansell","riccardo patrese","jean alesi","ayrton senna","alain prost","michael schumacher","mika hakkinen","andrea de cesaris","emanuele pirro","bertrand gachot"],
        "Gran Premio de Hungría":         ["ayrton senna","nigel mansell","riccardo patrese","gerhard berger","alain prost","jean alesi","roberto moreno","mika hakkinen","andrea de cesaris","thierry boutsen"],
        "Gran Premio de Bélgica":         ["ayrton senna","gerhard berger","nigel mansell","riccardo patrese","roberto moreno","michael schumacher","jean alesi","stefano modena","andrea de cesaris","mika hakkinen"],
        "Gran Premio de Italia":          ["nigel mansell","ayrton senna","alain prost","michael schumacher","jean alesi","gerhard berger","riccardo patrese","mika hakkinen","roberto moreno","andrea de cesaris"],
        "Gran Premio de Portugal":        ["riccardo patrese","ayrton senna","jean alesi","alain prost","thierry boutsen","nigel mansell","stefano modena","pierluigi martini","martin brundle","andrea de cesaris"],
        "Gran Premio de España":          ["nigel mansell","alain prost","riccardo patrese","ayrton senna","jean alesi","gerhard berger","michael schumacher","mika hakkinen","thierry boutsen","andrea de cesaris"],
        "Gran Premio de Japón":           ["gerhard berger","ayrton senna","riccardo patrese","alain prost","michael schumacher","jean alesi","mika hakkinen","nigel mansell","andrea de cesaris","pierluigi martini"],
        "Gran Premio de Australia":       ["ayrton senna","nigel mansell","gerhard berger","michael schumacher","martin brundle","thierry boutsen","riccardo patrese","jean alesi","mika hakkinen","roberto moreno"],
    },
    1992: {
        "Gran Premio de Sudáfrica":       ["nigel mansell","riccardo patrese","ayrton senna","mika hakkinen","martin brundle","gerhard berger","jean alesi","andrea de cesaris","pierluigi martini","thierry boutsen"],
        "Gran Premio de México":          ["nigel mansell","riccardo patrese","michael schumacher","ayrton senna","jean alesi","gerhard berger","martin brundle","ivan capelli","mika hakkinen","thierry boutsen"],
        "Gran Premio de Brasil":          ["nigel mansell","riccardo patrese","michael schumacher","ayrton senna","jean alesi","ivan capelli","martin brundle","mika hakkinen","thierry boutsen","andrea de cesaris"],
        "Gran Premio de España":          ["nigel mansell","michael schumacher","jean alesi","mika hakkinen","ayrton senna","riccardo patrese","gerhard berger","martin brundle","ivan capelli","andrea de cesaris"],
        "Gran Premio de San Marino":      ["nigel mansell","riccardo patrese","ayrton senna","gerhard berger","martin brundle","jean alesi","mika hakkinen","thierry boutsen","ivan capelli","pierluigi martini"],
        "Gran Premio de Mónaco":          ["ayrton senna","nigel mansell","riccardo patrese","michael schumacher","jean alesi","gerhard berger","martin brundle","mika hakkinen","paul belmondo","thierry boutsen"],
        "Gran Premio de Canadá":          ["gerhard berger","michael schumacher","jean alesi","ayrton senna","karl wendlinger","thierry boutsen","riccardo patrese","martin brundle","bertrand gachot","andrea de cesaris"],
        "Gran Premio de Francia":         ["nigel mansell","riccardo patrese","martin brundle","ayrton senna","mika hakkinen","gerhard berger","jean alesi","thierry boutsen","andrea de cesaris","ivan capelli"],
        "Gran Premio de Gran Bretaña":    ["nigel mansell","riccardo patrese","martin brundle","michael schumacher","gerhard berger","ayrton senna","mika hakkinen","thierry boutsen","bertrand gachot","jean alesi"],
        "Gran Premio de Alemania":        ["nigel mansell","ayrton senna","michael schumacher","riccardo patrese","jean alesi","martin brundle","mika hakkinen","thierry boutsen","ivan capelli","andrea de cesaris"],
        "Gran Premio de Hungría":         ["ayrton senna","nigel mansell","gerhard berger","michael schumacher","martin brundle","jean alesi","thierry boutsen","johnny herbert","bertrand gachot","ivan capelli"],
        "Gran Premio de Bélgica":         ["michael schumacher","nigel mansell","riccardo patrese","ayrton senna","martin brundle","gerhard berger","mika hakkinen","erik comas","thierry boutsen","jean alesi"],
        "Gran Premio de Italia":          ["ayrton senna","martin brundle","michael schumacher","gerhard berger","mika hakkinen","riccardo patrese","jean alesi","ivan capelli","thierry boutsen","andrea de cesaris"],
        "Gran Premio de Portugal":        ["nigel mansell","gerhard berger","ayrton senna","riccardo patrese","martin brundle","jean alesi","michael schumacher","thierry boutsen","mika hakkinen","ivan capelli"],
        "Gran Premio de Japón":           ["riccardo patrese","gerhard berger","martin brundle","ayrton senna","mika hakkinen","michael schumacher","thierry boutsen","andrea de cesaris","bertrand gachot","pierluigi martini"],
        "Gran Premio de Australia":       ["gerhard berger","michael schumacher","martin brundle","mark blundell","thierry boutsen","mika hakkinen","jean alesi","j.j. lehto","riccardo patrese","olivier grouillard"],
    },
    1993: {
        "Gran Premio de Sudáfrica":       ["alain prost","ayrton senna","mark blundell","michael schumacher","riccardo patrese","gerhard berger","johnny herbert","karl wendlinger","derek warwick","martin brundle"],
        "Gran Premio de Brasil":          ["ayrton senna","damon hill","mark blundell","michael schumacher","gerhard berger","johnny herbert","fabrizio barbazza","derek warwick","thierry boutsen","christian fittipaldi"],
        "Gran Premio de San Marino":      ["alain prost","michael schumacher","martin brundle","gerhard berger","johnny herbert","jean alesi","fabrizio barbazza","rubens barrichello","thierry boutsen","derek warwick"],
        "Gran Premio de España":          ["alain prost","ayrton senna","michael schumacher","damon hill","gerhard berger","jean alesi","johnny herbert","riccardo patrese","karl wendlinger","martin brundle"],
        "Gran Premio de Mónaco":          ["ayrton senna","damon hill","jean alesi","michael andretti","martin brundle","johnny herbert","mark blundell","derek warwick","christian fittipaldi","philippe alliot"],
        "Gran Premio de Canadá":          ["alain prost","michael schumacher","damon hill","gerhard berger","martin brundle","mark blundell","derek warwick","christian fittipaldi","jean alesi","johnny herbert"],
        "Gran Premio de Francia":         ["alain prost","damon hill","michael schumacher","gerhard berger","martin brundle","jean alesi","mark blundell","johnny herbert","rubens barrichello","derek warwick"],
        "Gran Premio de Gran Bretaña":    ["alain prost","michael schumacher","mark blundell","riccardo patrese","johnny herbert","martin brundle","rubens barrichello","derek warwick","christian fittipaldi","aguri suzuki"],
        "Gran Premio de Alemania":        ["alain prost","michael schumacher","mark blundell","damon hill","gerhard berger","jean alesi","karl wendlinger","johnny herbert","martin brundle","thierry boutsen"],
        "Gran Premio de Hungría":         ["damon hill","riccardo patrese","gerhard berger","derek warwick","mark blundell","thierry boutsen","aguri suzuki","jean alesi","christian fittipaldi","eddie irvine"],
        "Gran Premio de Bélgica":         ["damon hill","michael schumacher","alain prost","jean alesi","gerhard berger","riccardo patrese","martin brundle","johnny herbert","mika hakkinen","rubens barrichello"],
        "Gran Premio de Italia":          ["damon hill","michael schumacher","martin brundle","jean alesi","gerhard berger","riccardo patrese","derek warwick","christian fittipaldi","rubens barrichello","thierry boutsen"],
        "Gran Premio de Portugal":        ["michael schumacher","alain prost","damon hill","gerhard berger","jean alesi","martin brundle","mark blundell","johnny herbert","riccardo patrese","derek warwick"],
        "Gran Premio de Europa":          ["ayrton senna","alain prost","damon hill","michael schumacher","jean alesi","karl wendlinger","mika hakkinen","rubens barrichello","derek warwick","christian fittipaldi"],
        "Gran Premio de Japón":           ["ayrton senna","alain prost","mika hakkinen","damon hill","gerhard berger","johnny herbert","derek warwick","eddie irvine","aguri suzuki","michael andretti"],
        "Gran Premio de Australia":       ["ayrton senna","alain prost","damon hill","mika hakkinen","gerhard berger","jean alesi","riccardo patrese","johnny herbert","thierry boutsen","christian fittipaldi"],
    },
    1994: {
        "Gran Premio de Brasil":          ["michael schumacher","damon hill","jean alesi","rubens barrichello","mika hakkinen","nicola larini","eric bernard","olivier panis","gianni morbidelli","andrea de cesaris"],
        "Gran Premio del Pacífico":       ["michael schumacher","gerhard berger","rubens barrichello","christian fittipaldi","heinz-harold frentzen","olivier panis","eric bernard","gianni morbidelli","pierluigi martini","andrea de cesaris"],
        "Gran Premio de San Marino":      ["michael schumacher","nicola larini","mika hakkinen","damon hill","rubens barrichello","andrea de cesaris","eric bernard","olivier panis","gianni morbidelli","andrea montermini"],
        "Gran Premio de Mónaco":          ["michael schumacher","martin brundle","gerhard berger","andrea de cesaris","rubens barrichello","damon hill","olivier panis","mika hakkinen","eric bernard","heinz-harold frentzen"],
        "Gran Premio de España":          ["damon hill","michael schumacher","mark blundell","gerhard berger","jean alesi","rubens barrichello","david coulthard","pierluigi martini","heinz-harold frentzen","mika salo"],
        "Gran Premio de Canadá":          ["michael schumacher","damon hill","jean alesi","rubens barrichello","david coulthard","olivier panis","heinz-harold frentzen","bertrand gachot","eric bernard","pierluigi martini"],
        "Gran Premio de Francia":         ["michael schumacher","damon hill","gerhard berger","martin brundle","rubens barrichello","olivier panis","mika hakkinen","david coulthard","jean alesi","heinz-harold frentzen"],
        "Gran Premio de Gran Bretaña":    ["damon hill","michael schumacher","mika hakkinen","jos verstappen","martin brundle","david coulthard","olivier panis","christian fittipaldi","rubens barrichello","eric bernard"],
        "Gran Premio de Alemania":        ["gerhard berger","olivier panis","eric bernard","heinz-harold frentzen","christian fittipaldi","mika hakkinen","damon hill","rubens barrichello","pierluigi martini","jan magnussen"],
        "Gran Premio de Hungría":         ["michael schumacher","damon hill","jos verstappen","martin brundle","olivier panis","eric bernard","andrea montermini","mika salo","david coulthard","heinz-harold frentzen"],
        "Gran Premio de Bélgica":         ["damon hill","mika hakkinen","jos verstappen","david coulthard","rubens barrichello","jean alesi","olivier panis","heinz-harold frentzen","martin brundle","eric bernard"],
        "Gran Premio de Italia":          ["damon hill","gerhard berger","mika hakkinen","david coulthard","martin brundle","olivier panis","jean alesi","heinz-harold frentzen","pierluigi martini","eric bernard"],
        "Gran Premio de Portugal":        ["damon hill","david coulthard","mika hakkinen","gerhard berger","martin brundle","olivier panis","jean alesi","rubens barrichello","heinz-harold frentzen","christian fittipaldi"],
        "Gran Premio de Europa":          ["michael schumacher","damon hill","mika hakkinen","gerhard berger","rubens barrichello","martin brundle","olivier panis","nicola larini","heinz-harold frentzen","andrea de cesaris"],
        "Gran Premio de Japón":           ["damon hill","michael schumacher","jean alesi","mika hakkinen","rubens barrichello","nigel mansell","olivier panis","heinz-harold frentzen","christian fittipaldi","andrea de cesaris"],
        "Gran Premio de Australia":       ["nigel mansell","gerhard berger","martin brundle","rubens barrichello","mika hakkinen","olivier panis","gianni morbidelli","damon hill","aguri suzuki","david coulthard"],
    },
    1995: {
        "Gran Premio de Brasil":          ["michael schumacher","david coulthard","rubens barrichello","jean alesi","mika hakkinen","damon hill","johnny herbert","heinz-harold frentzen","olivier panis","pedro lamy"],
        "Gran Premio de Argentina":       ["damon hill","jean alesi","michael schumacher","rubens barrichello","mika hakkinen","heinz-harold frentzen","david coulthard","olivier panis","mark blundell","pierluigi martini"],
        "Gran Premio de San Marino":      ["damon hill","jean alesi","gerhard berger","michael schumacher","johnny herbert","rubens barrichello","heinz-harold frentzen","olivier panis","mika hakkinen","pierluigi martini"],
        "Gran Premio de España":          ["michael schumacher","johnny herbert","gerhard berger","rubens barrichello","mika hakkinen","olivier panis","jean alesi","damon hill","heinz-harold frentzen","pierluigi martini"],
        "Gran Premio de Mónaco":          ["michael schumacher","damon hill","gerhard berger","jean alesi","johnny herbert","heinz-harold frentzen","mika hakkinen","olivier panis","mark blundell","mika salo"],
        "Gran Premio de Canadá":          ["jean alesi","rubens barrichello","eddie irvine","olivier panis","mika hakkinen","heinz-harold frentzen","damon hill","michael schumacher","mark blundell","pierluigi martini"],
        "Gran Premio de Francia":         ["michael schumacher","damon hill","gerhard berger","rubens barrichello","johnny herbert","mika hakkinen","olivier panis","heinz-harold frentzen","jean alesi","mark blundell"],
        "Gran Premio de Gran Bretaña":    ["johnny herbert","jean alesi","damon hill","olivier panis","mika hakkinen","gerhard berger","rubens barrichello","mark blundell","karl wendlinger","mika salo"],
        "Gran Premio de Alemania":        ["michael schumacher","damon hill","gerhard berger","jean alesi","david coulthard","johnny herbert","olivier panis","mika hakkinen","heinz-harold frentzen","mark blundell"],
        "Gran Premio de Hungría":         ["damon hill","david coulthard","gerhard berger","michael schumacher","rubens barrichello","johnny herbert","mika hakkinen","heinz-harold frentzen","jean alesi","olivier panis"],
        "Gran Premio de Bélgica":         ["michael schumacher","damon hill","martin brundle","gerhard berger","jean alesi","rubens barrichello","olivier panis","mark blundell","heinz-harold frentzen","johnny herbert"],
        "Gran Premio de Italia":          ["johnny herbert","mika hakkinen","heinz-harold frentzen","martin brundle","gerhard berger","jean alesi","rubens barrichello","olivier panis","gianni morbidelli","andrea montermini"],
        "Gran Premio de Portugal":        ["david coulthard","michael schumacher","mika hakkinen","damon hill","gerhard berger","jean alesi","heinz-harold frentzen","olivier panis","johnny herbert","rubens barrichello"],
        "Gran Premio de Europa":          ["michael schumacher","damon hill","gerhard berger","jean alesi","mika hakkinen","olivier panis","rubens barrichello","johnny herbert","martin brundle","heinz-harold frentzen"],
        "Gran Premio del Pacífico":       ["michael schumacher","damon hill","rubens barrichello","jean alesi","gerhard berger","mika hakkinen","johnny herbert","heinz-harold frentzen","olivier panis","martin brundle"],
        "Gran Premio de Japón":           ["michael schumacher","mika hakkinen","damon hill","gerhard berger","johnny herbert","martin brundle","jean alesi","heinz-harold frentzen","olivier panis","rubens barrichello"],
        "Gran Premio de Australia":       ["damon hill","olivier panis","gianni morbidelli","rubens barrichello","mika hakkinen","gerhard berger","jean alesi","martin brundle","heinz-harold frentzen","michael schumacher"],
    },
    1996: {
        "Gran Premio de Australia":       ["damon hill","olivier panis","eddie irvine","gerhard berger","mika hakkinen","rubens barrichello","martin brundle","mika salo","johnny herbert","heinz-harold frentzen"],
        "Gran Premio de Brasil":          ["damon hill","jean alesi","michael schumacher","gerhard berger","rubens barrichello","olivier panis","mika hakkinen","mika salo","martin brundle","johnny herbert"],
        "Gran Premio de Argentina":       ["damon hill","jean alesi","michael schumacher","gerhard berger","rubens barrichello","eddie irvine","martin brundle","mika salo","johnny herbert","olivier panis"],
        "Gran Premio de Europa":          ["jacques villeneuve","michael schumacher","mika hakkinen","rubens barrichello","heinz-harold frentzen","mika salo","johnny herbert","martin brundle","oliver panis","pedro diniz"],
        "Gran Premio de San Marino":      ["damon hill","michael schumacher","gerhard berger","david coulthard","rubens barrichello","eddie irvine","mika hakkinen","heinz-harold frentzen","mika salo","olivier panis"],
        "Gran Premio de Mónaco":          ["olivier panis","david coulthard","johnny herbert","heinz-harold frentzen","mika salo","michael schumacher","rubens barrichello","pedro diniz","mika hakkinen","jarno trulli"],
        "Gran Premio de España":          ["michael schumacher","jean alesi","damon hill","rubens barrichello","mika hakkinen","gerhard berger","david coulthard","heinz-harold frentzen","mika salo","olivier panis"],
        "Gran Premio de Canadá":          ["damon hill","jean alesi","martin brundle","david coulthard","gerhard berger","mika hakkinen","mika salo","rubens barrichello","heinz-harold frentzen","pedro diniz"],
        "Gran Premio de Francia":         ["damon hill","jean alesi","michael schumacher","gerhard berger","mika hakkinen","rubens barrichello","david coulthard","heinz-harold frentzen","martin brundle","mika salo"],
        "Gran Premio de Gran Bretaña":    ["jacques villeneuve","gerhard berger","mika hakkinen","damon hill","david coulthard","rubens barrichello","eddie irvine","martin brundle","heinz-harold frentzen","jos verstappen"],
        "Gran Premio de Alemania":        ["damon hill","jean alesi","michael schumacher","gerhard berger","mika hakkinen","david coulthard","rubens barrichello","heinz-harold frentzen","olivier panis","mika salo"],
        "Gran Premio de Hungría":         ["jacques villeneuve","damon hill","jean alesi","michael schumacher","mika hakkinen","martin brundle","rubens barrichello","heinz-harold frentzen","david coulthard","mika salo"],
        "Gran Premio de Bélgica":         ["michael schumacher","jacques villeneuve","mika hakkinen","jean alesi","gerhard berger","rubens barrichello","martin brundle","olivier panis","pedro diniz","mika salo"],
        "Gran Premio de Italia":          ["michael schumacher","jean alesi","mika hakkinen","damon hill","gerhard berger","david coulthard","rubens barrichello","martin brundle","mika salo","heinz-harold frentzen"],
        "Gran Premio de Portugal":        ["jacques villeneuve","damon hill","michael schumacher","jean alesi","mika hakkinen","david coulthard","gerhard berger","rubens barrichello","mika salo","heinz-harold frentzen"],
        "Gran Premio de Japón":           ["damon hill","michael schumacher","mika hakkinen","gerhard berger","mika salo","johnny herbert","rubens barrichello","eddie irvine","martin brundle","olivier panis"],
    },
    1997: {
        "Gran Premio de Australia":       ["david coulthard","michael schumacher","mika hakkinen","eddie irvine","heinz-harold frentzen","ralf schumacher","damon hill","johnny herbert","mika salo","shinji nakano"],
        "Gran Premio de Brasil":          ["jacques villeneuve","gerhard berger","olivier panis","heinz-harold frentzen","johnny herbert","mika salo","ralf schumacher","pedro diniz","jarno trulli","ukyo katayama"],
        "Gran Premio de Argentina":       ["david coulthard","rubens barrichello","eddie irvine","ralf schumacher","mika hakkinen","shinji nakano","heinz-harold frentzen","giancarlo fisichella","damon hill","mika salo"],
        "Gran Premio de San Marino":      ["heinz-harold frentzen","michael schumacher","eddie irvine","mika hakkinen","ralf schumacher","giancarlo fisichella","jarno trulli","damon hill","mika salo","shinji nakano"],
        "Gran Premio de Mónaco":          ["michael schumacher","rubens barrichello","heinz-harold frentzen","eddie irvine","olivier panis","mika salo","jarno trulli","ralf schumacher","mika hakkinen","pedro diniz"],
        "Gran Premio de España":          ["jacques villeneuve","olivier panis","jean alesi","heinz-harold frentzen","johnny herbert","ralf schumacher","mika hakkinen","damon hill","giancarlo fisichella","mika salo"],
        "Gran Premio de Canadá":          ["michael schumacher","jean alesi","heinz-harold frentzen","giancarlo fisichella","eddie irvine","olivier panis","johnny herbert","mika hakkinen","ralf schumacher","pedro diniz"],
        "Gran Premio de Francia":         ["michael schumacher","heinz-harold frentzen","eddie irvine","mika hakkinen","ralf schumacher","giancarlo fisichella","damon hill","olivier panis","johnny herbert","rubens barrichello"],
        "Gran Premio de Gran Bretaña":    ["michael schumacher","mika hakkinen","heinz-harold frentzen","gerhard berger","david coulthard","alexander wurz","ralf schumacher","jarno trulli","rubens barrichello","eddie irvine"],
        "Gran Premio de Alemania":        ["gerhard berger","mika hakkinen","david coulthard","heinz-harold frentzen","olivier panis","damon hill","rubens barrichello","mika salo","ralf schumacher","shinji nakano"],
        "Gran Premio de Hungría":         ["jacques villeneuve","damon hill","johnny herbert","ralf schumacher","michael schumacher","heinz-harold frentzen","mika hakkinen","rubens barrichello","shinji nakano","mika salo"],
        "Gran Premio de Bélgica":         ["michael schumacher","giancarlo fisichella","heinz-harold frentzen","eddie irvine","ralf schumacher","mika hakkinen","damon hill","olivier panis","mika salo","shinji nakano"],
        "Gran Premio de Italia":          ["david coulthard","jean alesi","heinz-harold frentzen","mika hakkinen","eddie irvine","ralf schumacher","giancarlo fisichella","jarno trulli","mika salo","shinji nakano"],
        "Gran Premio de Austria":         ["jacques villeneuve","david coulthard","heinz-harold frentzen","eddie irvine","mika hakkinen","ralf schumacher","johnny herbert","olivier panis","mika salo","damon hill"],
        "Gran Premio de Luxemburgo":      ["mika hakkinen","michael schumacher","jacques villeneuve","heinz-harold frentzen","ralf schumacher","damon hill","giancarlo fisichella","jarno trulli","olivier panis","rubens barrichello"],
        "Gran Premio de Japón":           ["michael schumacher","heinz-harold frentzen","eddie irvine","mika hakkinen","ralf schumacher","damon hill","olivier panis","giancarlo fisichella","shinji nakano","pedro diniz"],
        "Gran Premio de Europa":          ["mika hakkinen","david coulthard","michael schumacher","heinz-harold frentzen","eddie irvine","mika salo","ralf schumacher","giancarlo fisichella","jarno trulli","olivier panis"],
    },
    1998: {
        "Gran Premio de Australia":       ["mika hakkinen","david coulthard","heinz-harold frentzen","eddie irvine","giancarlo fisichella","ralf schumacher","johnny herbert","mika salo","jarno trulli","olivier panis"],
        "Gran Premio de Brasil":          ["mika hakkinen","david coulthard","michael schumacher","alexander wurz","ralf schumacher","heinz-harold frentzen","giancarlo fisichella","johnny herbert","rubens barrichello","damon hill"],
        "Gran Premio de Argentina":       ["michael schumacher","mika hakkinen","eddie irvine","alexander wurz","ralf schumacher","giancarlo fisichella","johnny herbert","damon hill","rubens barrichello","mika salo"],
        "Gran Premio de San Marino":      ["david coulthard","michael schumacher","eddie irvine","mika hakkinen","giancarlo fisichella","ralf schumacher","jean alesi","heinz-harold frentzen","damon hill","mika salo"],
        "Gran Premio de España":          ["mika hakkinen","david coulthard","michael schumacher","giancarlo fisichella","ralf schumacher","eddie irvine","heinz-harold frentzen","damon hill","rubens barrichello","mika salo"],
        "Gran Premio de Mónaco":          ["mika hakkinen","giancarlo fisichella","eddie irvine","mika salo","heinz-harold frentzen","damon hill","pedro diniz","jos verstappen","olivier panis","ralf schumacher"],
        "Gran Premio de Canadá":          ["michael schumacher","giancarlo fisichella","eddie irvine","ralf schumacher","alexander wurz","damon hill","jean alesi","rubens barrichello","heinz-harold frentzen","mika salo"],
        "Gran Premio de Francia":         ["michael schumacher","eddie irvine","mika hakkinen","david coulthard","damon hill","giancarlo fisichella","olivier panis","ralf schumacher","heinz-harold frentzen","johnny herbert"],
        "Gran Premio de Gran Bretaña":    ["michael schumacher","mika hakkinen","eddie irvine","alexander wurz","damon hill","david coulthard","ralf schumacher","mika salo","heinz-harold frentzen","rubens barrichello"],
        "Gran Premio de Austria":         ["mika hakkinen","david coulthard","michael schumacher","eddie irvine","giancarlo fisichella","ralf schumacher","heinz-harold frentzen","damon hill","olivier panis","jean alesi"],
        "Gran Premio de Alemania":        ["mika hakkinen","david coulthard","giancarlo fisichella","eddie irvine","jean alesi","ralf schumacher","damon hill","mika salo","heinz-harold frentzen","rubens barrichello"],
        "Gran Premio de Hungría":         ["michael schumacher","david coulthard","jacques villeneuve","damon hill","ralf schumacher","heinz-harold frentzen","giancarlo fisichella","alexander wurz","olivier panis","pedro diniz"],
        "Gran Premio de Bélgica":         ["damon hill","ralf schumacher","jean alesi","michael schumacher","eddie irvine","mika hakkinen","giancarlo fisichella","david coulthard","heinz-harold frentzen","rubens barrichello"],
        "Gran Premio de Italia":          ["michael schumacher","eddie irvine","ralf schumacher","damon hill","mika hakkinen","giancarlo fisichella","heinz-harold frentzen","david coulthard","jean alesi","rubens barrichello"],
        "Gran Premio de Luxemburgo":      ["mika hakkinen","michael schumacher","david coulthard","eddie irvine","ralf schumacher","heinz-harold frentzen","giancarlo fisichella","jean alesi","damon hill","olivier panis"],
        "Gran Premio de Japón":           ["mika hakkinen","eddie irvine","david coulthard","damon hill","heinz-harold frentzen","michael schumacher","rubens barrichello","jan magnussen","ralf schumacher","shinji nakano"],
    },
    1999: {
        "Gran Premio de Australia":       ["eddie irvine","heinz-harold frentzen","mika hakkinen","ralf schumacher","giancarlo fisichella","damon hill","rubens barrichello","olivier panis","pedro diniz","pedro de la rosa"],
        "Gran Premio de Brasil":          ["mika hakkinen","eddie irvine","heinz-harold frentzen","ralf schumacher","giancarlo fisichella","johnny herbert","damon hill","rubens barrichello","mika salo","olivier panis"],
        "Gran Premio de San Marino":      ["michael schumacher","david coulthard","ralf schumacher","rubens barrichello","giancarlo fisichella","damon hill","olivier panis","mika salo","pedro diniz","jarno trulli"],
        "Gran Premio de Mónaco":          ["michael schumacher","eddie irvine","mika hakkinen","heinz-harold frentzen","ralf schumacher","giancarlo fisichella","alexander wurz","damon hill","pedro diniz","jarno trulli"],
        "Gran Premio de España":          ["mika hakkinen","david coulthard","michael schumacher","ralf schumacher","heinz-harold frentzen","giancarlo fisichella","rubens barrichello","damon hill","jarno trulli","olivier panis"],
        "Gran Premio de Canadá":          ["mika hakkinen","giancarlo fisichella","michael schumacher","heinz-harold frentzen","damon hill","ralf schumacher","rubens barrichello","david coulthard","olivier panis","pedro diniz"],
        "Gran Premio de Francia":         ["heinz-harold frentzen","rubens barrichello","mika hakkinen","ralf schumacher","giancarlo fisichella","david coulthard","damon hill","mika salo","olivier panis","jarno trulli"],
        "Gran Premio de Gran Bretaña":    ["david coulthard","eddie irvine","ralf schumacher","heinz-harold frentzen","damon hill","mika salo","jarno trulli","alexander wurz","olivier panis","pedro diniz"],
        "Gran Premio de Austria":         ["eddie irvine","david coulthard","mika hakkinen","ralf schumacher","giancarlo fisichella","heinz-harold frentzen","mika salo","damon hill","olivier panis","jarno trulli"],
        "Gran Premio de Alemania":        ["eddie irvine","mika hakkinen","david coulthard","ralf schumacher","heinz-harold frentzen","rubens barrichello","giancarlo fisichella","jarno trulli","olivier panis","pedro de la rosa"],
        "Gran Premio de Hungría":         ["mika hakkinen","damon hill","david coulthard","ralf schumacher","rubens barrichello","giancarlo fisichella","heinz-harold frentzen","olivier panis","pedro diniz","jarno trulli"],
        "Gran Premio de Bélgica":         ["david coulthard","mika hakkinen","heinz-harold frentzen","ralf schumacher","giancarlo fisichella","jarno trulli","rubens barrichello","damon hill","olivier panis","pedro de la rosa"],
        "Gran Premio de Italia":          ["heinz-harold frentzen","ralf schumacher","mika salo","rubens barrichello","david coulthard","giancarlo fisichella","damon hill","olivier panis","pedro de la rosa","alexander wurz"],
        "Gran Premio de Europa":          ["johnny herbert","rubens barrichello","mika hakkinen","ralf schumacher","giancarlo fisichella","mika salo","pedro de la rosa","damon hill","heinz-harold frentzen","jarno trulli"],
        "Gran Premio de Malasia":         ["eddie irvine","michael schumacher","mika hakkinen","david coulthard","heinz-harold frentzen","ralf schumacher","giancarlo fisichella","rubens barrichello","jarno trulli","damon hill"],
        "Gran Premio de Japón":           ["mika hakkinen","michael schumacher","eddie irvine","heinz-harold frentzen","ralf schumacher","johnny herbert","giancarlo fisichella","rubens barrichello","mika salo","alex zanardi"],
    },
    2000: {
        "Gran Premio de Australia":       ["michael schumacher","rubens barrichello","ralf schumacher","heinz-harold frentzen","jenson button","giancarlo fisichella","mika hakkinen","david coulthard","pedro diniz","nick heidfeld"],
        "Gran Premio de Brasil":          ["michael schumacher","giancarlo fisichella","rubens barrichello","ralf schumacher","mika hakkinen","heinz-harold frentzen","jenson button","eddie irvine","david coulthard","pedro diniz"],
        "Gran Premio de San Marino":      ["michael schumacher","david coulthard","rubens barrichello","mika hakkinen","heinz-harold frentzen","ralf schumacher","jenson button","giancarlo fisichella","jarno trulli","nick heidfeld"],
        "Gran Premio de Gran Bretaña":    ["david coulthard","michael schumacher","rubens barrichello","mika hakkinen","heinz-harold frentzen","jenson button","ralf schumacher","eddie irvine","giancarlo fisichella","pedro diniz"],
        "Gran Premio de España":          ["mika hakkinen","michael schumacher","david coulthard","ralf schumacher","rubens barrichello","giancarlo fisichella","jenson button","heinz-harold frentzen","jarno trulli","nick heidfeld"],
        "Gran Premio de Europa":          ["michael schumacher","mika hakkinen","rubens barrichello","david coulthard","giancarlo fisichella","jenson button","ralf schumacher","heinz-harold frentzen","nick heidfeld","pedro diniz"],
        "Gran Premio de Mónaco":          ["david coulthard","rubens barrichello","giancarlo fisichella","michael schumacher","eddie irvine","jenson button","mika salo","heinz-harold frentzen","nick heidfeld","tarso marques"],
        "Gran Premio de Canadá":          ["michael schumacher","rubens barrichello","giancarlo fisichella","mika hakkinen","ralf schumacher","heinz-harold frentzen","jenson button","jarno trulli","david coulthard","eddie irvine"],
        "Gran Premio de Francia":         ["david coulthard","mika hakkinen","rubens barrichello","michael schumacher","ralf schumacher","giancarlo fisichella","heinz-harold frentzen","jenson button","jarno trulli","nick heidfeld"],
        "Gran Premio de Austria":         ["mika hakkinen","david coulthard","rubens barrichello","michael schumacher","giancarlo fisichella","ralf schumacher","heinz-harold frentzen","jenson button","nick heidfeld","jarno trulli"],
        "Gran Premio de Alemania":        ["rubens barrichello","mika hakkinen","david coulthard","jenson button","giancarlo fisichella","ralf schumacher","heinz-harold frentzen","jarno trulli","nick heidfeld","pedro diniz"],
        "Gran Premio de Hungría":         ["mika hakkinen","michael schumacher","david coulthard","rubens barrichello","ralf schumacher","giancarlo fisichella","jenson button","heinz-harold frentzen","nick heidfeld","jarno trulli"],
        "Gran Premio de Bélgica":         ["mika hakkinen","michael schumacher","ralf schumacher","david coulthard","rubens barrichello","giancarlo fisichella","jenson button","heinz-harold frentzen","jarno trulli","pedro diniz"],
        "Gran Premio de Italia":          ["michael schumacher","mika hakkinen","ralf schumacher","rubens barrichello","jenson button","heinz-harold frentzen","eddie irvine","giancarlo fisichella","mika salo","pedro diniz"],
        "Gran Premio de Estados Unidos":  ["michael schumacher","rubens barrichello","heinz-harold frentzen","david coulthard","giancarlo fisichella","ralf schumacher","mika hakkinen","nick heidfeld","jenson button","pedro diniz"],
        "Gran Premio de Japón":           ["michael schumacher","mika hakkinen","david coulthard","rubens barrichello","ralf schumacher","giancarlo fisichella","jenson button","nick heidfeld","heinz-harold frentzen","eddie irvine"],
        "Gran Premio de Malasia":         ["michael schumacher","rubens barrichello","david coulthard","mika hakkinen","giancarlo fisichella","ralf schumacher","heinz-harold frentzen","jenson button","jarno trulli","pedro diniz"],
    },
    2001: {
        "Gran Premio de Australia": ["michael schumacher","david coulthard","rubens barrichello","nick heidfeld","kimi raikkonen","jacques villeneuve","ralf schumacher","jarno trulli","mika hakkinen","jean alesi"],
        "Gran Premio de Malasia": ["michael schumacher","rubens barrichello","david coulthard","ralf schumacher","mika hakkinen","jarno trulli","nick heidfeld","kimi raikkonen","jacques villeneuve","olivier panis"],
        "Gran Premio de Brasil": ["david coulthard","michael schumacher","nick heidfeld","rubens barrichello","jarno trulli","juan pablo montoya","ralf schumacher","kimi raikkonen","jacques villeneuve","mika hakkinen"],
        "Gran Premio de San Marino": ["ralf schumacher","david coulthard","rubens barrichello","michael schumacher","mika hakkinen","nick heidfeld","jarno trulli","kimi raikkonen","jean alesi","giancarlo fisichella"],
        "Gran Premio de España": ["michael schumacher","juan pablo montoya","kimi raikkonen","ralf schumacher","mika hakkinen","jarno trulli","nick heidfeld","rubens barrichello","jenson button","olivier panis"],
        "Gran Premio de Austria": ["david coulthard","michael schumacher","rubens barrichello","ralf schumacher","mika hakkinen","jarno trulli","nick heidfeld","kimi raikkonen","jenson button","jean alesi"],
        "Gran Premio de Mónaco": ["michael schumacher","rubens barrichello","eddie irvine","jarno trulli","david coulthard","ralf schumacher","nick heidfeld","jenson button","kimi raikkonen","jean alesi"],
        "Gran Premio de Canadá": ["ralf schumacher","michael schumacher","mika hakkinen","david coulthard","rubens barrichello","jarno trulli","nick heidfeld","kimi raikkonen","jenson button","jean alesi"],
        "Gran Premio de Europa": ["michael schumacher","ralf schumacher","rubens barrichello","juan pablo montoya","david coulthard","jarno trulli","nick heidfeld","jenson button","kimi raikkonen","eddie irvine"],
        "Gran Premio de Francia": ["michael schumacher","ralf schumacher","rubens barrichello","juan pablo montoya","david coulthard","jarno trulli","nick heidfeld","jenson button","kimi raikkonen","jean alesi"],
        "Gran Premio de Gran Bretaña": ["mika hakkinen","michael schumacher","rubens barrichello","juan pablo montoya","ralf schumacher","david coulthard","jarno trulli","nick heidfeld","jenson button","kimi raikkonen"],
        "Gran Premio de Alemania": ["ralf schumacher","rubens barrichello","jarno trulli","nick heidfeld","david coulthard","juan pablo montoya","michael schumacher","jenson button","kimi raikkonen","eddie irvine"],
        "Gran Premio de Hungría": ["michael schumacher","david coulthard","rubens barrichello","ralf schumacher","mika hakkinen","nick heidfeld","jarno trulli","kimi raikkonen","jenson button","jean alesi"],
        "Gran Premio de Bélgica": ["michael schumacher","david coulthard","giancarlo fisichella","nick heidfeld","jarno trulli","jenson button","ralf schumacher","kimi raikkonen","jean alesi","eddie irvine"],
        "Gran Premio de Italia": ["juan pablo montoya","rubens barrichello","ralf schumacher","michael schumacher","david coulthard","jarno trulli","nick heidfeld","jenson button","kimi raikkonen","giancarlo fisichella"],
        "Gran Premio de Estados Unidos": ["mika hakkinen","michael schumacher","david coulthard","rubens barrichello","juan pablo montoya","ralf schumacher","jarno trulli","nick heidfeld","jenson button","kimi raikkonen"],
        "Gran Premio de Japón": ["michael schumacher","juan pablo montoya","david coulthard","rubens barrichello","ralf schumacher","mika hakkinen","jarno trulli","nick heidfeld","jenson button","kimi raikkonen"]
    },
    2002: {
        "Gran Premio de Australia": ["michael schumacher","juan pablo montoya","kimi raikkonen","ralf schumacher","jarno trulli","jenson button","david coulthard","mika salo","nick heidfeld","felipe massa"],
        "Gran Premio de Malasia": ["ralf schumacher","juan pablo montoya","michael schumacher","jacques villeneuve","olivier panis","mika salo","mark webber","jenson button","nick heidfeld","kimi raikkonen"],
        "Gran Premio de Brasil": ["michael schumacher","ralf schumacher","david coulthard","juan pablo montoya","jenson button","jarno trulli","nick heidfeld","felipe massa","heinz harald frentzen","kimi raikkonen"],
        "Gran Premio de San Marino": ["michael schumacher","ralf schumacher","juan pablo montoya","jenson button","david coulthard","jarno trulli","nick heidfeld","felipe massa","heinz harald frentzen","mark webber"],
        "Gran Premio de España": ["michael schumacher","juan pablo montoya","kimi raikkonen","ralf schumacher","rubens barrichello","jenson button","david coulthard","jarno trulli","nick heidfeld","felipe massa"],
        "Gran Premio de Austria": ["michael schumacher","rubens barrichello","juan pablo montoya","ralf schumacher","mika hakkinen","jenson button","david coulthard","jarno trulli","nick heidfeld","felipe massa"],
        "Gran Premio de Mónaco": ["david coulthard","michael schumacher","ralf schumacher","juan pablo montoya","rubens barrichello","jarno trulli","jenson button","nick heidfeld","felipe massa","olivier panis"],
        "Gran Premio de Canadá": ["michael schumacher","ralf schumacher","juan pablo montoya","rubens barrichello","jenson button","jarno trulli","nick heidfeld","felipe massa","david coulthard","olivier panis"],
        "Gran Premio de Europa": ["rubens barrichello","ralf schumacher","juan pablo montoya","michael schumacher","jenson button","jarno trulli","nick heidfeld","felipe massa","david coulthard","olivier panis"],
        "Gran Premio de Gran Bretaña": ["michael schumacher","rubens barrichello","juan pablo montoya","kimi raikkonen","ralf schumacher","jarno trulli","jenson button","david coulthard","nick heidfeld","felipe massa"],
        "Gran Premio de Francia": ["michael schumacher","kimi raikkonen","jarno trulli","rubens barrichello","ralf schumacher","juan pablo montoya","jenson button","david coulthard","nick heidfeld","felipe massa"],
        "Gran Premio de Alemania": ["michael schumacher","juan pablo montoya","david coulthard","ralf schumacher","rubens barrichello","jarno trulli","jenson button","nick heidfeld","felipe massa","mark webber"],
        "Gran Premio de Hungría": ["rubens barrichello","michael schumacher","ralf schumacher","kimi raikkonen","david coulthard","juan pablo montoya","jarno trulli","jenson button","nick heidfeld","felipe massa"],
        "Gran Premio de Bélgica": ["michael schumacher","ralf schumacher","juan pablo montoya","kimi raikkonen","rubens barrichello","jarno trulli","jenson button","david coulthard","nick heidfeld","felipe massa"],
        "Gran Premio de Italia": ["rubens barrichello","michael schumacher","juan pablo montoya","ralf schumacher","kimi raikkonen","jarno trulli","jenson button","david coulthard","nick heidfeld","felipe massa"],
        "Gran Premio de Estados Unidos": ["rubens barrichello","michael schumacher","ralf schumacher","juan pablo montoya","kimi raikkonen","jarno trulli","jenson button","nick heidfeld","felipe massa","david coulthard"],
        "Gran Premio de Japón": ["michael schumacher","rubens barrichello","kimi raikkonen","juan pablo montoya","ralf schumacher","jarno trulli","jenson button","nick heidfeld","felipe massa","david coulthard"]
    },
    2003: {
        "Gran Premio de Australia": ["david coulthard","juan pablo montoya","kimi raikkonen","michael schumacher","ralf schumacher","jarno trulli","mark webber","heinz harald frentzen","jacques villeneuve","ralf firman"],
        "Gran Premio de Malasia": ["kimi raikkonen","rubens barrichello","fernando alonso","ralf schumacher","michael schumacher","jarno trulli","david coulthard","jenson button","nick heidfeld","olivier panis"],
        "Gran Premio de Brasil": ["giancarlo fisichella","kimi raikkonen","fernando alonso","david coulthard","jarno trulli","mark webber","nick heidfeld","antonio pizzonia","ralf firman","christiano da matta"],
        "Gran Premio de San Marino": ["michael schumacher","kimi raikkonen","rubens barrichello","ralf schumacher","fernando alonso","david coulthard","jarno trulli","mark webber","jenson button","giancarlo fisichella"],
        "Gran Premio de España": ["michael schumacher","fernando alonso","rubens barrichello","ralf schumacher","david coulthard","jarno trulli","jenson button","giancarlo fisichella","mark webber","olivier panis"],
        "Gran Premio de Austria": ["michael schumacher","kimi raikkonen","rubens barrichello","ralf schumacher","juan pablo montoya","david coulthard","jarno trulli","jenson button","mark webber","nick heidfeld"],
        "Gran Premio de Mónaco": ["juan pablo montoya","kimi raikkonen","michael schumacher","ralf schumacher","jarno trulli","jenson button","david coulthard","fernando alonso","mark webber","olivier panis"],
        "Gran Premio de Canadá": ["michael schumacher","ralf schumacher","juan pablo montoya","rubens barrichello","jarno trulli","david coulthard","fernando alonso","jenson button","mark webber","nick heidfeld"],
        "Gran Premio de Europa": ["ralf schumacher","juan pablo montoya","rubens barrichello","michael schumacher","jarno trulli","fernando alonso","jenson button","mark webber","david coulthard","nick heidfeld"],
        "Gran Premio de Francia": ["ralf schumacher","juan pablo montoya","michael schumacher","kimi raikkonen","jarno trulli","jenson button","david coulthard","fernando alonso","mark webber","nick heidfeld"],
        "Gran Premio de Gran Bretaña": ["rubens barrichello","juan pablo montoya","kimi raikkonen","ralf schumacher","michael schumacher","david coulthard","jarno trulli","fernando alonso","mark webber","jenson button"],
        "Gran Premio de Alemania": ["juan pablo montoya","david coulthard","ralf schumacher","rubens barrichello","jarno trulli","jenson button","mark webber","nick heidfeld","fernando alonso","olivier panis"],
        "Gran Premio de Hungría": ["fernando alonso","kimi raikkonen","juan pablo montoya","ralf schumacher","michael schumacher","rubens barrichello","jarno trulli","mark webber","jenson button","nick heidfeld"],
        "Gran Premio de Italia": ["michael schumacher","juan pablo montoya","rubens barrichello","fernando alonso","ralf schumacher","jarno trulli","david coulthard","jenson button","mark webber","nick heidfeld"],
        "Gran Premio de Estados Unidos": ["michael schumacher","kimi raikkonen","heinz harald frentzen","nick heidfeld","juan pablo montoya","rubens barrichello","jarno trulli","jenson button","mark webber","ralf schumacher"],
        "Gran Premio de Japón": ["rubens barrichello","kimi raikkonen","david coulthard","juan pablo montoya","ralf schumacher","fernando alonso","jenson button","jarno trulli","takuma sato","giancarlo fisichella"]
    },
    2004: {
        "Gran Premio de Australia": ["michael schumacher","rubens barrichello","fernando alonso","ralf schumacher","juan pablo montoya","jenson button","takuma sato","mark webber","felipe massa","olivier panis"],
        "Gran Premio de Malasia": ["michael schumacher","juan pablo montoya","jenson button","fernando alonso","ralf schumacher","takuma sato","mark webber","felipe massa","giancarlo fisichella","christian klien"],
        "Gran Premio de Bahréin": ["michael schumacher","rubens barrichello","jenson button","jarno trulli","takuma sato","fernando alonso","ralf schumacher","juan pablo montoya","mark webber","felipe massa"],
        "Gran Premio de San Marino": ["michael schumacher","jenson button","juan pablo montoya","ralf schumacher","jarno trulli","takuma sato","rubens barrichello","fernando alonso","felipe massa","mark webber"],
        "Gran Premio de España": ["michael schumacher","rubens barrichello","jarno trulli","jenson button","takuma sato","ralf schumacher","fernando alonso","juan pablo montoya","felipe massa","giancarlo fisichella"],
        "Gran Premio de Mónaco": ["jarno trulli","jenson button","rubens barrichello","fernando alonso","juan pablo montoya","ralf schumacher","takuma sato","felipe massa","david coulthard","olivier panis"],
        "Gran Premio de Europa": ["michael schumacher","rubens barrichello","jenson button","takuma sato","fernando alonso","juan pablo montoya","ralf schumacher","jarno trulli","felipe massa","david coulthard"],
        "Gran Premio de Canadá": ["michael schumacher","rubens barrichello","jenson button","fernando alonso","takuma sato","juan pablo montoya","ralf schumacher","mark webber","giancarlo fisichella","felipe massa"],
        "Gran Premio de Estados Unidos": ["michael schumacher","rubens barrichello","takuma sato","jenson button","juan pablo montoya","ralf schumacher","david coulthard","jarno trulli","olivier panis","christian klien"],
        "Gran Premio de Francia": ["michael schumacher","fernando alonso","rubens barrichello","jarno trulli","jenson button","takuma sato","juan pablo montoya","ralf schumacher","mark webber","felipe massa"],
        "Gran Premio de Gran Bretaña": ["michael schumacher","rubens barrichello","jenson button","fernando alonso","juan pablo montoya","ralf schumacher","takuma sato","jarno trulli","felipe massa","mark webber"],
        "Gran Premio de Alemania": ["michael schumacher","jenson button","fernando alonso","takuma sato","juan pablo montoya","ralf schumacher","rubens barrichello","mark webber","felipe massa","giancarlo fisichella"],
        "Gran Premio de Hungría": ["michael schumacher","rubens barrichello","fernando alonso","takuma sato","jenson button","juan pablo montoya","ralf schumacher","mark webber","felipe massa","giancarlo fisichella"],
        "Gran Premio de Bélgica": ["kimi raikkonen","michael schumacher","rubens barrichello","fernando alonso","juan pablo montoya","jenson button","takuma sato","ralf schumacher","mark webber","felipe massa"],
        "Gran Premio de Italia": ["rubens barrichello","michael schumacher","jenson button","takuma sato","juan pablo montoya","fernando alonso","ralf schumacher","jarno trulli","mark webber","felipe massa"],
        "Gran Premio de China": ["rubens barrichello","jenson button","kimi raikkonen","fernando alonso","juan pablo montoya","michael schumacher","takuma sato","felipe massa","mark webber","giancarlo fisichella"],
        "Gran Premio de Japón": ["michael schumacher","rubens barrichello","jenson button","takuma sato","kimi raikkonen","fernando alonso","ralf schumacher","mark webber","felipe massa","giancarlo fisichella"],
        "Gran Premio de Brasil": ["juan pablo montoya","kimi raikkonen","rubens barrichello","fernando alonso","ralf schumacher","takuma sato","felipe massa","jenson button","christian klien","giancarlo fisichella"]
    },
    2005: {
        "Gran Premio de Australia": ["giancarlo fisichella","rubens barrichello","fernando alonso","jarno trulli","nick heidfeld","ralf schumacher","mark webber","david coulthard","christijan albers","patrick friesacher"],
        "Gran Premio de Malasia": ["fernando alonso","jarno trulli","nick heidfeld","ralf schumacher","juan pablo montoya","mark webber","david coulthard","tiago monteiro","narain karthikeyan","christijan albers"],
        "Gran Premio de Bahréin": ["fernando alonso","jarno trulli","kimi raikkonen","michael schumacher","nick heidfeld","mark webber","ralf schumacher","david coulthard","felipe massa","jacques villeneuve"],
        "Gran Premio de San Marino": ["fernando alonso","michael schumacher","alexander wurz","jarno trulli","kimi raikkonen","nick heidfeld","mark webber","ralf schumacher","giancarlo fisichella","jenson button"],
        "Gran Premio de España": ["kimi raikkonen","fernando alonso","jarno trulli","ralf schumacher","michael schumacher","giancarlo fisichella","mark webber","nick heidfeld","david coulthard","felipe massa"],
        "Gran Premio de Mónaco": ["kimi raikkonen","nick heidfeld","mark webber","fernando alonso","juan pablo montoya","ralf schumacher","michael schumacher","rubens barrichello","giancarlo fisichella","felipe massa"],
        "Gran Premio de Europa": ["fernando alonso","nick heidfeld","rubens barrichello","mark webber","ralf schumacher","jacques villeneuve","jarno trulli","david coulthard","christijan albers","tiago monteiro"],
        "Gran Premio de Canadá": ["kimi raikkonen","michael schumacher","rubens barrichello","jenson button","giancarlo fisichella","juan pablo montoya","ralf schumacher","mark webber","felipe massa","jacques villeneuve"],
        "Gran Premio de Estados Unidos": ["michael schumacher","rubens barrichello","tiago monteiro","narain karthikeyan","christijan albers","patrick friesacher"],
        "Gran Premio de Francia": ["fernando alonso","kimi raikkonen","michael schumacher","rubens barrichello","jenson button","giancarlo fisichella","ralf schumacher","jarno trulli","mark webber","felipe massa"],
        "Gran Premio de Gran Bretaña": ["juan pablo montoya","fernando alonso","kimi raikkonen","giancarlo fisichella","jenson button","rubens barrichello","ralf schumacher","david coulthard","christijan albers","felipe massa"],
        "Gran Premio de Alemania": ["fernando alonso","juan pablo montoya","jenson button","giancarlo fisichella","kimi raikkonen","michael schumacher","ralf schumacher","felipe massa","mark webber","nick heidfeld"],
        "Gran Premio de Hungría": ["kimi raikkonen","michael schumacher","ralf schumacher","juan pablo montoya","giancarlo fisichella","jarno trulli","jenson button","mark webber","nick heidfeld","david coulthard"],
        "Gran Premio de Turquía": ["kimi raikkonen","fernando alonso","juan pablo montoya","giancarlo fisichella","ralf schumacher","mark webber","jenson button","david coulthard","christijan albers","tiago monteiro"],
        "Gran Premio de Italia": ["juan pablo montoya","fernando alonso","giancarlo fisichella","kimi raikkonen","ralf schumacher","rubens barrichello","jenson button","felipe massa","michael schumacher","jacques villeneuve"],
        "Gran Premio de Bélgica": ["kimi raikkonen","giancarlo fisichella","fernando alonso","juan pablo montoya","jenson button","mark webber","ralf schumacher","felipe massa","michael schumacher","rubens barrichello"],
        "Gran Premio de Brasil": ["juan pablo montoya","kimi raikkonen","fernando alonso","michael schumacher","giancarlo fisichella","rubens barrichello","jenson button","ralf schumacher","felipe massa","christijan albers"],
        "Gran Premio de Japón": ["kimi raikkonen","giancarlo fisichella","fernando alonso","mark webber","jenson button","michael schumacher","ralf schumacher","david coulthard","felipe massa","jacques villeneuve"],
        "Gran Premio de China": ["fernando alonso","kimi raikkonen","ralf schumacher","juan pablo montoya","giancarlo fisichella","michael schumacher","rubens barrichello","jenson button","mark webber","felipe massa"]
    },
    2006: {
        "Gran Premio de Bahréin": ["fernando alonso","michael schumacher","kimi raikkonen","jenson button","juan pablo montoya","felipe massa","mark webber","nico rosberg","christian klien","jacques villeneuve"],
        "Gran Premio de Malasia": ["giancarlo fisichella","fernando alonso","jenson button","nick heidfeld","mark webber","jacques villeneuve","juan pablo montoya","felipe massa","christian klien","nico rosberg"],
        "Gran Premio de Australia": ["fernando alonso","kimi raikkonen","ralf schumacher","nick heidfeld","giancarlo fisichella","jacques villeneuve","mark webber","nico rosberg","christian klien","rubens barrichello"],
        "Gran Premio de San Marino": ["michael schumacher","fernando alonso","juan pablo montoya","felipe massa","kimi raikkonen","jenson button","mark webber","nico rosberg","christian klien","jacques villeneuve"],
        "Gran Premio de Europa": ["michael schumacher","fernando alonso","felipe massa","giancarlo fisichella","kimi raikkonen","rubens barrichello","jacques villeneuve","ralf schumacher","nick heidfeld","david coulthard"],
        "Gran Premio de España": ["fernando alonso","michael schumacher","giancarlo fisichella","felipe massa","kimi raikkonen","rubens barrichello","jenson button","nick heidfeld","mark webber","david coulthard"],
        "Gran Premio de Mónaco": ["fernando alonso","juan pablo montoya","david coulthard","michael schumacher","giancarlo fisichella","nick heidfeld","ralf schumacher","rubens barrichello","jacques villeneuve","felipe massa"],
        "Gran Premio de Gran Bretaña": ["fernando alonso","michael schumacher","kimi raikkonen","felipe massa","giancarlo fisichella","ralf schumacher","jenson button","jarno trulli","nick heidfeld","mark webber"],
        "Gran Premio de Canadá": ["fernando alonso","michael schumacher","kimi raikkonen","giancarlo fisichella","felipe massa","jarno trulli","ralf schumacher","nick heidfeld","david coulthard","rubens barrichello"],
        "Gran Premio de Estados Unidos": ["michael schumacher","felipe massa","giancarlo fisichella","jarno trulli","rubens barrichello","david coulthard","tonio liuzzi","scott speed","christijan albers","tiago monteiro"],
        "Gran Premio de Francia": ["michael schumacher","fernando alonso","felipe massa","ralf schumacher","kimi raikkonen","giancarlo fisichella","nick heidfeld","jarno trulli","david coulthard","rubens barrichello"],
        "Gran Premio de Alemania": ["michael schumacher","felipe massa","kimi raikkonen","jenson button","fernando alonso","ralf schumacher","nick heidfeld","david coulthard","christijan albers","tiago monteiro"],
        "Gran Premio de Hungría": ["jenson button","pedro de la rosa","nick heidfeld","rubens barrichello","david coulthard","ralf schumacher","felipe massa","giancarlo fisichella","tonio liuzzi","christijan albers"],
        "Gran Premio de Turquía": ["felipe massa","fernando alonso","michael schumacher","giancarlo fisichella","kimi raikkonen","nick heidfeld","jenson button","pedro de la rosa","mark webber","nico rosberg"],
        "Gran Premio de Italia": ["michael schumacher","kimi raikkonen","robert kubica","giancarlo fisichella","fernando alonso","felipe massa","jarno trulli","nick heidfeld","rubens barrichello","jenson button"],
        "Gran Premio de China": ["michael schumacher","fernando alonso","giancarlo fisichella","rubens barrichello","jenson button","pedro de la rosa","nick heidfeld","mark webber","nico rosberg","tonio liuzzi"],
        "Gran Premio de Japón": ["fernando alonso","felipe massa","giancarlo fisichella","jenson button","kimi raikkonen","pedro de la rosa","mark webber","rubens barrichello","nick heidfeld","david coulthard"],
        "Gran Premio de Brasil": ["felipe massa","fernando alonso","jenson button","michael schumacher","kimi raikkonen","giancarlo fisichella","rubens barrichello","nick heidfeld","robert kubica","scott speed"]
    },
    2007: {
        "Gran Premio de Australia": ["kimi raikkonen","fernando alonso","lewis hamilton","nick heidfeld","giancarlo fisichella","felipe massa","nico rosberg","ralf schumacher","robert kubica","heikki kovalainen"],
        "Gran Premio de Malasia": ["fernando alonso","lewis hamilton","kimi raikkonen","nick heidfeld","robert kubica","jarno trulli","ralf schumacher","mark webber","giancarlo fisichella","nico rosberg"],
        "Gran Premio de Bahréin": ["felipe massa","lewis hamilton","kimi raikkonen","nick heidfeld","fernando alonso","heikki kovalainen","jarno trulli","ralf schumacher","mark webber","alexander wurz"],
        "Gran Premio de España": ["felipe massa","lewis hamilton","fernando alonso","robert kubica","giancarlo fisichella","jarno trulli","nick heidfeld","david coulthard","nico rosberg","alexander wurz"],
        "Gran Premio de Mónaco": ["fernando alonso","lewis hamilton","felipe massa","giancarlo fisichella","robert kubica","nick heidfeld","alexander wurz","jarno trulli","mark webber","ralf schumacher"],
        "Gran Premio de Canadá": ["lewis hamilton","nick heidfeld","alexander wurz","heikki kovalainen","kimi raikkonen","fernando alonso","nico rosberg","jarno trulli","takuma sato","ralf schumacher"],
        "Gran Premio de Estados Unidos": ["lewis hamilton","fernando alonso","felipe massa","nick heidfeld","heikki kovalainen","jarno trulli","mark webber","nico rosberg","alexander wurz","vitantonio liuzzi"],
        "Gran Premio de Francia": ["kimi raikkonen","felipe massa","lewis hamilton","robert kubica","nick heidfeld","heikki kovalainen","giancarlo fisichella","jarno trulli","nico rosberg","david coulthard"],
        "Gran Premio de Gran Bretaña": ["kimi raikkonen","fernando alonso","lewis hamilton","felipe massa","nick heidfeld","robert kubica","heikki kovalainen","giancarlo fisichella","nico rosberg","alexander wurz"],
        "Gran Premio de Europa": ["fernando alonso","felipe massa","mark webber","alexander wurz","david coulthard","nick heidfeld","robert kubica","heikki kovalainen","nico rosberg","ralf schumacher"],
        "Gran Premio de Hungría": ["lewis hamilton","kimi raikkonen","nick heidfeld","fernando alonso","robert kubica","ralf schumacher","nico rosberg","heikki kovalainen","jarno trulli","mark webber"],
        "Gran Premio de Turquía": ["felipe massa","kimi raikkonen","fernando alonso","lewis hamilton","nick heidfeld","nico rosberg","robert kubica","heikki kovalainen","giancarlo fisichella","jarno trulli"],
        "Gran Premio de Italia": ["fernando alonso","lewis hamilton","kimi raikkonen","nick heidfeld","felipe massa","robert kubica","nico rosberg","heikki kovalainen","jarno trulli","sebastian vettel"],
        "Gran Premio de Bélgica": ["kimi raikkonen","felipe massa","fernando alonso","lewis hamilton","nick heidfeld","nico rosberg","mark webber","heikki kovalainen","robert kubica","jarno trulli"],
        "Gran Premio de Japón": ["lewis hamilton","heikki kovalainen","kimi raikkonen","david coulthard","giancarlo fisichella","felipe massa","fernando alonso","alexander wurz","vitantonio liuzzi","jenson button"],
        "Gran Premio de China": ["kimi raikkonen","fernando alonso","felipe massa","lewis hamilton","nick heidfeld","robert kubica","nico rosberg","heikki kovalainen","rubens barrichello","sebastian vettel"],
        "Gran Premio de Brasil": ["kimi raikkonen","felipe massa","fernando alonso","nick heidfeld","nico rosberg","robert kubica","heikki kovalainen","jarno trulli","mark webber","sebastian vettel"]
    },
    2008: {
        "Gran Premio de Australia": ["lewis hamilton","nick heidfeld","nico rosberg","fernando alonso","heikki kovalainen","kazuki nakajima","sebastien bourdais","kimi raikkonen","timo glock","jarno trulli"],
        "Gran Premio de Malasia": ["kimi raikkonen","robert kubica","heikki kovalainen","jarno trulli","lewis hamilton","nick heidfeld","mark webber","fernando alonso","david coulthard","jenson button"],
        "Gran Premio de Bahréin": ["felipe massa","kimi raikkonen","robert kubica","nick heidfeld","heikki kovalainen","jarno trulli","mark webber","nico rosberg","lewis hamilton","timo glock"],
        "Gran Premio de España": ["kimi raikkonen","felipe massa","lewis hamilton","robert kubica","mark webber","jenson button","kazuki nakajima","jarno trulli","sebastien bourdais","nico rosberg"],
        "Gran Premio de Turquía": ["felipe massa","lewis hamilton","kimi raikkonen","robert kubica","fernando alonso","nick heidfeld","heikki kovalainen","nico rosberg","sebastien bourdais","jarno trulli"],
        "Gran Premio de Mónaco": ["lewis hamilton","robert kubica","felipe massa","mark webber","sebastian vettel","rubens barrichello","kazuki nakajima","heikki kovalainen","kimi raikkonen","adrian sutil"],
        "Gran Premio de Canadá": ["robert kubica","nick heidfeld","david coulthard","timo glock","felipe massa","jarno trulli","rubens barrichello","sebastian vettel","nico rosberg","fernando alonso"],
        "Gran Premio de Francia": ["felipe massa","kimi raikkonen","jarno trulli","heikki kovalainen","robert kubica","mark webber","fernando alonso","lewis hamilton","nico rosberg","sebastian vettel"],
        "Gran Premio de Gran Bretaña": ["lewis hamilton","nick heidfeld","rubens barrichello","kimi raikkonen","heikki kovalainen","fernando alonso","jarno trulli","kazuki nakajima","nico rosberg","sebastian vettel"],
        "Gran Premio de Alemania": ["lewis hamilton","nelson piquet","felipe massa","nick heidfeld","heikki kovalainen","kimi raikkonen","robert kubica","sebastian vettel","jarno trulli","nico rosberg"],
        "Gran Premio de Hungría": ["heikki kovalainen","timo glock","kimi raikkonen","fernando alonso","lewis hamilton","nelson piquet","jarno trulli","robert kubica","nico rosberg","felipe massa"],
        "Gran Premio de Europa": ["felipe massa","lewis hamilton","robert kubica","heikki kovalainen","jarno trulli","sebastian vettel","timo glock","nico rosberg","fernando alonso","nick heidfeld"],
        "Gran Premio de Bélgica": ["felipe massa","nick heidfeld","lewis hamilton","fernando alonso","sebastian vettel","robert kubica","nico rosberg","heikki kovalainen","timo glock","mark webber"],
        "Gran Premio de Italia": ["sebastian vettel","heikki kovalainen","robert kubica","fernando alonso","nick heidfeld","felipe massa","lewis hamilton","mark webber","timo glock","nico rosberg"],
        "Gran Premio de Singapur": ["fernando alonso","nico rosberg","lewis hamilton","timo glock","sebastian vettel","nick heidfeld","david coulthard","kazuki nakajima","jarno trulli","jenson button"],
        "Gran Premio de Japón": ["fernando alonso","robert kubica","kimi raikkonen","nelson piquet","felipe massa","mark webber","sebastian vettel","rubens barrichello","timo glock","jarno trulli"],
        "Gran Premio de China": ["lewis hamilton","felipe massa","kimi raikkonen","fernando alonso","heikki kovalainen","sebastian vettel","jarno trulli","sebastien bourdais","timo glock","nick heidfeld"],
        "Gran Premio de Brasil": ["felipe massa","fernando alonso","kimi raikkonen","sebastian vettel","lewis hamilton","jarno trulli","mark webber","nico rosberg","robert kubica","timo glock"]
    },
    2009: {
        "Gran Premio de Australia": ["jenson button","rubens barrichello","jarno trulli","timo glock","fernando alonso","nico rosberg","sebastien buemi","sebastian bourdais","adrian sutil","nick heidfeld"],
        "Gran Premio de Malasia": ["jenson button","nick heidfeld","timo glock","jarno trulli","rubens barrichello","mark webber","lewis hamilton","nico rosberg","felipe massa","sebastian vettel"],
        "Gran Premio de China": ["sebastian vettel","mark webber","jenson button","rubens barrichello","heikki kovalainen","lewis hamilton","timo glock","fernando alonso","nico rosberg","sebastien buemi"],
        "Gran Premio de Bahréin": ["jenson button","sebastian vettel","jarno trulli","lewis hamilton","rubens barrichello","kimi raikkonen","timo glock","fernando alonso","nico rosberg","nelson piquet"],
        "Gran Premio de España": ["jenson button","rubens barrichello","mark webber","sebastian vettel","fernando alonso","felipe massa","nico rosberg","lewis hamilton","timo glock","nick heidfeld"],
        "Gran Premio de Mónaco": ["jenson button","rubens barrichello","kimi raikkonen","felipe massa","mark webber","nico rosberg","fernando alonso","sebastian vettel","timo glock","nick heidfeld"],
        "Gran Premio de Turquía": ["jenson button","mark webber","sebastian vettel","jarno trulli","nico rosberg","felipe massa","robert kubica","timo glock","nick heidfeld","fernando alonso"],
        "Gran Premio de Gran Bretaña": ["sebastian vettel","mark webber","rubens barrichello","jenson button","nico rosberg","jarno trulli","kimi raikkonen","timo glock","fernando alonso","lewis hamilton"],
        "Gran Premio de Alemania": ["mark webber","sebastian vettel","felipe massa","nico rosberg","jenson button","rubens barrichello","fernando alonso","heikki kovalainen","timo glock","nick heidfeld"],
        "Gran Premio de Hungría": ["lewis hamilton","kimi raikkonen","mark webber","nico rosberg","heikki kovalainen","timo glock","jenson button","jarno trulli","kazuki nakajima","rubens barrichello"],
        "Gran Premio de Europa": ["rubens barrichello","lewis hamilton","kimi raikkonen","heikki kovalainen","nico rosberg","fernando alonso","jenson button","robert kubica","timo glock","nick heidfeld"],
        "Gran Premio de Bélgica": ["kimi raikkonen","giancarlo fisichella","sebastian vettel","robert kubica","nick heidfeld","heikki kovalainen","rubens barrichello","nico rosberg","mark webber","timo glock"],
        "Gran Premio de Italia": ["rubens barrichello","jenson button","kimi raikkonen","lewis hamilton","adrian sutil","fernando alonso","heikki kovalainen","nico rosberg","sebastian vettel","tonio liuzzi"],
        "Gran Premio de Singapur": ["lewis hamilton","timo glock","fernando alonso","sebastian vettel","jenson button","rubens barrichello","heikki kovalainen","robert kubica","nico rosberg","jarno trulli"],
        "Gran Premio de Japón": ["sebastian vettel","jarno trulli","lewis hamilton","kimi raikkonen","nico rosberg","nick heidfeld","rubens barrichello","jenson button","adrian sutil","tonio liuzzi"],
        "Gran Premio de Brasil": ["mark webber","robert kubica","lewis hamilton","sebastian vettel","jenson button","kimi raikkonen","sebastien buemi","rubens barrichello","nico rosberg","jarno trulli"],
        "Gran Premio de Abu Dabi": ["sebastian vettel","mark webber","jenson button","rubens barrichello","nico rosberg","robert kubica","nick heidfeld","kamui kobayashi","jarno trulli","jaime alguersuari"]
    },
    2010: {
        "Gran Premio de Bahréin": ["fernando alonso","felipe massa","lewis hamilton","sebastian vettel","nico rosberg","michael schumacher","jenson button","mark webber","vitantonio liuzzi","rubens barrichello"],
        "Gran Premio de Australia": ["jenson button","robert kubica","felipe massa","fernando alonso","nico rosberg","lewis hamilton","vitantonio liuzzi","rubens barrichello","mark webber","michael schumacher"],
        "Gran Premio de Malasia": ["sebastian vettel","mark webber","nico rosberg","robert kubica","adrian sutil","lewis hamilton","felipe massa","jenson button","jaime alguersuari","nico hulkenberg"],
        "Gran Premio de China": ["jenson button","lewis hamilton","nico rosberg","fernando alonso","robert kubica","sebastian vettel","vitaly petrov","mark webber","felipe massa","michael schumacher"],
        "Gran Premio de España": ["mark webber","fernando alonso","sebastian vettel","michael schumacher","jenson button","felipe massa","adrian sutil","robert kubica","rubens barrichello","jaime alguersuari"],
        "Gran Premio de Mónaco": ["mark webber","sebastian vettel","robert kubica","felipe massa","lewis hamilton","vitantonio liuzzi","rubens barrichello","fernando alonso","nico rosberg","karun chandhok"],
        "Gran Premio de Turquía": ["lewis hamilton","jenson button","mark webber","sebastian vettel","michael schumacher","nico rosberg","robert kubica","felipe massa","fernando alonso","vitaly petrov"],
        "Gran Premio de Canadá": ["lewis hamilton","jenson button","fernando alonso","sebastian vettel","mark webber","nico rosberg","robert kubica","vitantonio liuzzi","rubens barrichello","adrian sutil"],
        "Gran Premio de Europa": ["sebastian vettel","lewis hamilton","jenson button","rubens barrichello","robert kubica","adrian sutil","kamui kobayashi","fernando alonso","sebastien buemi","nico rosberg"],
        "Gran Premio de Gran Bretaña": ["mark webber","lewis hamilton","nico rosberg","jenson button","sebastian vettel","adrian sutil","michael schumacher","nico hulkenberg","rubens barrichello","kamui kobayashi"],
        "Gran Premio de Alemania": ["fernando alonso","felipe massa","sebastian vettel","lewis hamilton","jenson button","mark webber","robert kubica","nico rosberg","michael schumacher","vitaly petrov"],
        "Gran Premio de Hungría": ["mark webber","fernando alonso","sebastian vettel","felipe massa","vitaly petrov","nico hulkenberg","pedro de la rosa","jenson button","kamui kobayashi","rubens barrichello"],
        "Gran Premio de Bélgica": ["lewis hamilton","mark webber","robert kubica","felipe massa","adrian sutil","nico rosberg","michael schumacher","kamui kobayashi","vitaly petrov","nico hulkenberg"],
        "Gran Premio de Italia": ["fernando alonso","jenson button","felipe massa","lewis hamilton","nico rosberg","nico hulkenberg","robert kubica","michael schumacher","rubens barrichello","sebastien buemi"],
        "Gran Premio de Singapur": ["fernando alonso","sebastian vettel","mark webber","lewis hamilton","nico rosberg","robert kubica","felipe massa","vitantonio liuzzi","rubens barrichello","nico hulkenberg"],
        "Gran Premio de Japón": ["sebastian vettel","mark webber","fernando alonso","jenson button","lewis hamilton","michael schumacher","kamui kobayashi","nico rosberg","rubens barrichello","sebastien buemi"],
        "Gran Premio de Corea": ["fernando alonso","lewis hamilton","felipe massa","michael schumacher","robert kubica","vitantonio liuzzi","rubens barrichello","kamui kobayashi","nick heidfeld","nico hulkenberg"],
        "Gran Premio de Brasil": ["sebastian vettel","mark webber","fernando alonso","lewis hamilton","jenson button","nico rosberg","michael schumacher","nico hulkenberg","robert kubica","kamui kobayashi"],
        "Gran Premio de Abu Dabi": ["sebastian vettel","lewis hamilton","jenson button","nico rosberg","robert kubica","vitantonio liuzzi","felipe massa","fernando alonso","mark webber","jaime alguersuari"]
    },
    2011: {
        "Gran Premio de Australia": ["sebastian vettel","lewis hamilton","vitaly petrov","fernando alonso","mark webber","jenson button","sergio perez","kamui kobayashi","felipe massa","sebastien buemi"],
        "Gran Premio de Malasia": ["sebastian vettel","jenson button","nick heidfeld","mark webber","felipe massa","fernando alonso","kamui kobayashi","lewis hamilton","michael schumacher","paul di resta"],
        "Gran Premio de China": ["lewis hamilton","sebastian vettel","mark webber","jenson button","nico rosberg","felipe massa","fernando alonso","michael schumacher","vitaly petrov","kamui kobayashi"],
        "Gran Premio de Turquía": ["sebastian vettel","mark webber","fernando alonso","lewis hamilton","nico rosberg","jenson button","nick heidfeld","vitaly petrov","sebastien buemi","kamui kobayashi"],
        "Gran Premio de España": ["sebastian vettel","lewis hamilton","jenson button","mark webber","fernando alonso","michael schumacher","nico rosberg","nick heidfeld","sergio perez","kamui kobayashi"],
        "Gran Premio de Mónaco": ["sebastian vettel","fernando alonso","jenson button","mark webber","lewis hamilton","nico rosberg","felipe massa","pastor maldonado","sergio perez","adrian sutil"],
        "Gran Premio de Canadá": ["jenson button","sebastian vettel","mark webber","michael schumacher","vitaly petrov","felipe massa","kamui kobayashi","jaime alguersuari","rubens barrichello","sebastien buemi"],
        "Gran Premio de Europa": ["sebastian vettel","fernando alonso","mark webber","lewis hamilton","felipe massa","jenson button","nico rosberg","jaime alguersuari","adrian sutil","nick heidfeld"],
        "Gran Premio de Gran Bretaña": ["fernando alonso","sebastian vettel","mark webber","lewis hamilton","felipe massa","nico rosberg","sergio perez","nick heidfeld","kamui kobayashi","michael schumacher"],
        "Gran Premio de Alemania": ["lewis hamilton","fernando alonso","mark webber","sebastian vettel","felipe massa","nico rosberg","kamui kobayashi","nick heidfeld","sebastien buemi","adrian sutil"],
        "Gran Premio de Hungría": ["jenson button","sebastian vettel","fernando alonso","lewis hamilton","mark webber","felipe massa","paul di resta","sebastien buemi","nico rosberg","jaime alguersuari"],
        "Gran Premio de Bélgica": ["sebastian vettel","mark webber","jenson button","fernando alonso","michael schumacher","nico rosberg","adrian sutil","felipe massa","vitaly petrov","pastor maldonado"],
        "Gran Premio de Italia": ["sebastian vettel","jenson button","fernando alonso","lewis hamilton","michael schumacher","felipe massa","jaime alguersuari","paul di resta","bruno senna","kamui kobayashi"],
        "Gran Premio de Singapur": ["sebastian vettel","jenson button","mark webber","fernando alonso","lewis hamilton","paul di resta","nico rosberg","adrian sutil","felipe massa","sergio perez"],
        "Gran Premio de Japón": ["jenson button","fernando alonso","sebastian vettel","mark webber","lewis hamilton","michael schumacher","felipe massa","sergio perez","vitaly petrov","nico rosberg"],
        "Gran Premio de Corea": ["sebastian vettel","lewis hamilton","mark webber","jenson button","fernando alonso","felipe massa","jaime alguersuari","nico rosberg","sebastien buemi","paul di resta"],
        "Gran Premio de India": ["sebastian vettel","jenson button","fernando alonso","mark webber","michael schumacher","nico rosberg","lewis hamilton","adrian sutil","sergio perez","kamui kobayashi"],
        "Gran Premio de Abu Dabi": ["lewis hamilton","fernando alonso","jenson button","mark webber","sebastian vettel","felipe massa","sergio perez","bruno senna","paul di resta","kamui kobayashi"],
        "Gran Premio de Brasil": ["mark webber","sebastian vettel","jenson button","fernando alonso","lewis hamilton","felipe massa","adrian sutil","nico rosberg","kamui kobayashi","vitaly petrov"]
    },
    2012: {
        "Gran Premio de Australia": ["jenson button","sebastian vettel","lewis hamilton","mark webber","fernando alonso","kamui kobayashi","kimi raikkonen","sergio perez","daniel ricciardo","paul di resta"],
        "Gran Premio de Malasia": ["fernando alonso","sergio perez","lewis hamilton","mark webber","kimi raikkonen","bruno senna","paul di resta","jean eric vergne","nico hulkenberg","michael schumacher"],
        "Gran Premio de China": ["nico rosberg","jenson button","lewis hamilton","mark webber","sebastian vettel","romain grosjean","bruno senna","pastor maldonado","fernando alonso","kamui kobayashi"],
        "Gran Premio de Bahréin": ["sebastian vettel","kimi raikkonen","romain grosjean","mark webber","nico rosberg","paul di resta","fernando alonso","lewis hamilton","felipe massa","michael schumacher"],
        "Gran Premio de España": ["pastor maldonado","fernando alonso","kimi raikkonen","romain grosjean","kamui kobayashi","sebastian vettel","nico rosberg","lewis hamilton","jenson button","nico hulkenberg"],
        "Gran Premio de Mónaco": ["mark webber","nico rosberg","fernando alonso","sebastian vettel","lewis hamilton","felipe massa","paul di resta","nico hulkenberg","kimi raikkonen","bruno senna"],
        "Gran Premio de Canadá": ["lewis hamilton","romain grosjean","sergio perez","sebastian vettel","fernando alonso","nico rosberg","mark webber","kimi raikkonen","kamui kobayashi","felipe massa"],
        "Gran Premio de Europa": ["fernando alonso","kimi raikkonen","michael schumacher","mark webber","nico hulkenberg","nico rosberg","paul di resta","jenson button","sergio perez","daniel ricciardo"],
        "Gran Premio de Gran Bretaña": ["mark webber","fernando alonso","sebastian vettel","felipe massa","kimi raikkonen","romain grosjean","michael schumacher","lewis hamilton","bruno senna","jenson button"],
        "Gran Premio de Alemania": ["fernando alonso","sebastian vettel","jenson button","kimi raikkonen","kamui kobayashi","felipe massa","pastor maldonado","nico hulkenberg","nico rosberg","sergio perez"],
        "Gran Premio de Hungría": ["lewis hamilton","kimi raikkonen","romain grosjean","sebastian vettel","fernando alonso","jenson button","bruno senna","mark webber","nico rosberg","paul di resta"],
        "Gran Premio de Bélgica": ["jenson button","sebastian vettel","kimi raikkonen","nico hulkenberg","felipe massa","mark webber","michael schumacher","jean eric vergne","daniel ricciardo","paul di resta"],
        "Gran Premio de Italia": ["lewis hamilton","sergio perez","fernando alonso","felipe massa","kimi raikkonen","michael schumacher","nico rosberg","paul di resta","kamui kobayashi","bruno senna"],
        "Gran Premio de Singapur": ["sebastian vettel","jenson button","fernando alonso","paul di resta","nico rosberg","kimi raikkonen","romain grosjean","felipe massa","daniel ricciardo","nico hulkenberg"],
        "Gran Premio de Japón": ["sebastian vettel","felipe massa","kamui kobayashi","jenson button","lewis hamilton","kimi raikkonen","nico hulkenberg","pastor maldonado","mark webber","daniel ricciardo"],
        "Gran Premio de Corea": ["sebastian vettel","mark webber","fernando alonso","felipe massa","kimi raikkonen","nico hulkenberg","romain grosjean","jean eric vergne","daniel ricciardo","sergio perez"],
        "Gran Premio de India": ["sebastian vettel","fernando alonso","mark webber","lewis hamilton","jenson button","felipe massa","nico hulkenberg","kimi raikkonen","sergio perez","daniel ricciardo"],
        "Gran Premio de Abu Dabi": ["kimi raikkonen","fernando alonso","sebastian vettel","mark webber","lewis hamilton","jenson button","nico hulkenberg","pastor maldonado","bruno senna","paul di resta"],
        "Gran Premio de Estados Unidos": ["lewis hamilton","sebastian vettel","fernando alonso","felipe massa","jenson button","kimi raikkonen","romain grosjean","nico hulkenberg","bruno senna","paul di resta"],
        "Gran Premio de Brasil": ["jenson button","fernando alonso","felipe massa","mark webber","nico hulkenberg","sebastian vettel","michael schumacher","jean eric vergne","kamui kobayashi","kimi raikkonen"]
    },
    2013: {
        "Gran Premio de Australia": ["kimi raikkonen","fernando alonso","sebastian vettel","felipe massa","lewis hamilton","mark webber","adrian sutil","paul di resta","jenson button","romain grosjean"],
        "Gran Premio de Malasia": ["sebastian vettel","mark webber","lewis hamilton","nico rosberg","felipe massa","romain grosjean","kimi raikkonen","nico hulkenberg","sergio perez","jean eric vergne"],
        "Gran Premio de China": ["fernando alonso","kimi raikkonen","lewis hamilton","sebastian vettel","jenson button","felipe massa","daniel ricciardo","paul di resta","romain grosjean","nico hulkenberg"],
        "Gran Premio de Bahréin": ["sebastian vettel","kimi raikkonen","romain grosjean","paul di resta","lewis hamilton","sergio perez","mark webber","fernando alonso","nico rosberg","jenson button"],
        "Gran Premio de España": ["fernando alonso","kimi raikkonen","felipe massa","sebastian vettel","mark webber","nico rosberg","paul di resta","jenson button","sergio perez","daniel ricciardo"],
        "Gran Premio de Mónaco": ["nico rosberg","sebastian vettel","mark webber","lewis hamilton","adrian sutil","jenson button","fernando alonso","jean eric vergne","paul di resta","kimi raikkonen"],
        "Gran Premio de Canadá": ["sebastian vettel","fernando alonso","lewis hamilton","mark webber","nico rosberg","jean eric vergne","paul di resta","adrian sutil","felipe massa","kimi raikkonen"],
        "Gran Premio de Gran Bretaña": ["nico rosberg","mark webber","fernando alonso","lewis hamilton","kimi raikkonen","felipe massa","adrian sutil","daniel ricciardo","paul di resta","nico hulkenberg"],
        "Gran Premio de Alemania": ["sebastian vettel","kimi raikkonen","romain grosjean","fernando alonso","lewis hamilton","jenson button","mark webber","sergio perez","nico rosberg","nico hulkenberg"],
        "Gran Premio de Hungría": ["lewis hamilton","kimi raikkonen","sebastian vettel","mark webber","fernando alonso","romain grosjean","jenson button","felipe massa","sergio perez","pastor maldonado"],
        "Gran Premio de Bélgica": ["sebastian vettel","fernando alonso","lewis hamilton","nico rosberg","mark webber","jenson button","felipe massa","romain grosjean","adrian sutil","daniel ricciardo"],
        "Gran Premio de Italia": ["sebastian vettel","fernando alonso","mark webber","felipe massa","nico hulkenberg","nico rosberg","daniel ricciardo","romain grosjean","lewis hamilton","jenson button"],
        "Gran Premio de Singapur": ["sebastian vettel","fernando alonso","kimi raikkonen","nico rosberg","lewis hamilton","felipe massa","jenson button","sergio perez","nico hulkenberg","adrian sutil"],
        "Gran Premio de Corea": ["sebastian vettel","kimi raikkonen","romain grosjean","nico hulkenberg","lewis hamilton","fernando alonso","nico rosberg","jenson button","felipe massa","sergio perez"],
        "Gran Premio de Japón": ["sebastian vettel","mark webber","romain grosjean","fernando alonso","kimi raikkonen","nico hulkenberg","esteban gutierrez","nico rosberg","jenson button","felipe massa"],
        "Gran Premio de India": ["sebastian vettel","nico rosberg","romain grosjean","mark webber","fernando alonso","lewis hamilton","kimi raikkonen","paul di resta","adrian sutil","sergio perez"],
        "Gran Premio de Abu Dabi": ["sebastian vettel","mark webber","nico rosberg","romain grosjean","fernando alonso","lewis hamilton","paul di resta","adrian sutil","sergio perez","jean eric vergne"],
        "Gran Premio de Estados Unidos": ["sebastian vettel","romain grosjean","mark webber","lewis hamilton","fernando alonso","nico hulkenberg","sergio perez","valtteri bottas","nico rosberg","jenson button"],
        "Gran Premio de Brasil": ["sebastian vettel","mark webber","fernando alonso","jenson button","nico rosberg","sergio perez","felipe massa","nico hulkenberg","lewis hamilton","daniel ricciardo"]
    },
    2014: {
        "Gran Premio de Australia": ["nico rosberg","kevin magnussen","jenson button","fernando alonso","valtteri bottas","nico hulkenberg","kimi raikkonen","jean eric vergne","daniil kvyat","sergio perez"],
        "Gran Premio de Malasia": ["lewis hamilton","nico rosberg","sebastian vettel","fernando alonso","nico hulkenberg","jenson button","felipe massa","valtteri bottas","kevin magnussen","daniil kvyat"],
        "Gran Premio de Bahréin": ["lewis hamilton","nico rosberg","sergio perez","daniel ricciardo","nico hulkenberg","sebastian vettel","felipe massa","valtteri bottas","fernando alonso","kimi raikkonen"],
        "Gran Premio de China": ["lewis hamilton","nico rosberg","fernando alonso","daniel ricciardo","sebastian vettel","nico hulkenberg","valtteri bottas","kimi raikkonen","sergio perez","daniil kvyat"],
        "Gran Premio de España": ["lewis hamilton","nico rosberg","daniel ricciardo","sebastian vettel","valtteri bottas","fernando alonso","kimi raikkonen","romain grosjean","sergio perez","nico hulkenberg"],
        "Gran Premio de Mónaco": ["nico rosberg","lewis hamilton","daniel ricciardo","fernando alonso","nico hulkenberg","jenson button","felipe massa","romain grosjean","jules bianchi","kevin magnussen"],
        "Gran Premio de Canadá": ["daniel ricciardo","nico rosberg","sebastian vettel","jenson button","nico hulkenberg","fernando alonso","valtteri bottas","jean eric vergne","kevin magnussen","kimi raikkonen"],
        "Gran Premio de Austria": ["nico rosberg","lewis hamilton","valtteri bottas","felipe massa","fernando alonso","sergio perez","kevin magnussen","daniel ricciardo","nico hulkenberg","kimi raikkonen"],
        "Gran Premio de Gran Bretaña": ["lewis hamilton","valtteri bottas","daniel ricciardo","jenson button","sebastian vettel","fernando alonso","kevin magnussen","nico hulkenberg","daniil kvyat","jean eric vergne"],
        "Gran Premio de Alemania": ["nico rosberg","valtteri bottas","lewis hamilton","sebastian vettel","fernando alonso","daniel ricciardo","nico hulkenberg","jenson button","kevin magnussen","sergio perez"],
        "Gran Premio de Hungría": ["daniel ricciardo","fernando alonso","lewis hamilton","nico rosberg","felipe massa","kimi raikkonen","sebastian vettel","valtteri bottas","jean eric vergne","jenson button"],
        "Gran Premio de Bélgica": ["daniel ricciardo","nico rosberg","valtteri bottas","kimi raikkonen","sebastian vettel","fernando alonso","sergio perez","daniil kvyat","nico hulkenberg","jean eric vergne"],
        "Gran Premio de Italia": ["lewis hamilton","nico rosberg","felipe massa","valtteri bottas","daniel ricciardo","sebastian vettel","sergio perez","jenson button","kimi raikkonen","kevin magnussen"],
        "Gran Premio de Singapur": ["lewis hamilton","sebastian vettel","daniel ricciardo","fernando alonso","felipe massa","valtteri bottas","jean eric vergne","sergio perez","nico hulkenberg","kevin magnussen"],
        "Gran Premio de Japón": ["lewis hamilton","nico rosberg","sebastian vettel","daniel ricciardo","valtteri bottas","felipe massa","jenson button","nico hulkenberg","jean eric vergne","sergio perez"],
        "Gran Premio de Rusia": ["lewis hamilton","nico rosberg","valtteri bottas","jenson button","kevin magnussen","fernando alonso","daniel ricciardo","sebastian vettel","kimi raikkonen","sergio perez"],
        "Gran Premio de Estados Unidos": ["lewis hamilton","nico rosberg","daniel ricciardo","felipe massa","valtteri bottas","fernando alonso","sebastian vettel","kevin magnussen","jean eric vergne","sergio perez"],
        "Gran Premio de Brasil": ["nico rosberg","lewis hamilton","felipe massa","jenson button","sebastian vettel","fernando alonso","valtteri bottas","nico hulkenberg","kevin magnussen","sergio perez"],
        "Gran Premio de Abu Dabi": ["lewis hamilton","felipe massa","valtteri bottas","daniel ricciardo","jenson button","nico rosberg","nico hulkenberg","sergio perez","sebastian vettel","fernando alonso"]
    },
    2015: {
        "Gran Premio de Australia": ["lewis hamilton","nico rosberg","sebastian vettel","felipe massa","felipe nasr","daniel ricciardo","nico hulkenberg","marcus ericsson","carlos sainz","sergio perez"],
        "Gran Premio de Malasia": ["sebastian vettel","lewis hamilton","nico rosberg","kimi raikkonen","valtteri bottas","felipe massa","max verstappen","carlos sainz","daniel ricciardo","romain grosjean"],
        "Gran Premio de China": ["lewis hamilton","nico rosberg","sebastian vettel","kimi raikkonen","valtteri bottas","felipe massa","daniel ricciardo","romain grosjean","felipe nasr","marcus ericsson"],
        "Gran Premio de Bahréin": ["lewis hamilton","kimi raikkonen","nico rosberg","valtteri bottas","sebastian vettel","daniel ricciardo","romain grosjean","sergio perez","daniil kvyat","felipe massa"],
        "Gran Premio de España": ["nico rosberg","lewis hamilton","sebastian vettel","valtteri bottas","kimi raikkonen","felipe massa","daniel ricciardo","romain grosjean","carlos sainz","daniil kvyat"],
        "Gran Premio de Mónaco": ["nico rosberg","sebastian vettel","lewis hamilton","daniil kvyat","daniel ricciardo","kimi raikkonen","sergio perez","felipe nasr","carlos sainz","jenson button"],
        "Gran Premio de Canadá": ["lewis hamilton","nico rosberg","valtteri bottas","kimi raikkonen","sebastian vettel","felipe massa","pastor maldonado","nico hulkenberg","daniil kvyat","romain grosjean"],
        "Gran Premio de Austria": ["nico rosberg","lewis hamilton","felipe massa","valtteri bottas","sebastian vettel","felipe nasr","nico hulkenberg","daniel ricciardo","sergio perez","marcus ericsson"],
        "Gran Premio de Gran Bretaña": ["lewis hamilton","nico rosberg","sebastian vettel","felipe massa","valtteri bottas","daniil kvyat","nico hulkenberg","kimi raikkonen","sergio perez","fernando alonso"],
        "Gran Premio de Hungría": ["sebastian vettel","daniil kvyat","daniel ricciardo","max verstappen","fernando alonso","lewis hamilton","romain grosjean","nico rosberg","jenson button","marcus ericsson"],
        "Gran Premio de Bélgica": ["lewis hamilton","nico rosberg","romain grosjean","daniil kvyat","sergio perez","felipe massa","kimi raikkonen","max verstappen","valtteri bottas","marcus ericsson"],
        "Gran Premio de Italia": ["lewis hamilton","sebastian vettel","felipe massa","valtteri bottas","kimi raikkonen","sergio perez","nico hulkenberg","daniel ricciardo","marcus ericsson","felipe nasr"],
        "Gran Premio de Singapur": ["sebastian vettel","daniel ricciardo","kimi raikkonen","nico rosberg","valtteri bottas","daniil kvyat","sergio perez","max verstappen","carlos sainz","pastor maldonado"],
        "Gran Premio de Japón": ["lewis hamilton","nico rosberg","sebastian vettel","valtteri bottas","kimi raikkonen","nico hulkenberg","romain grosjean","felipe massa","max verstappen","carlos sainz"],
        "Gran Premio de Rusia": ["lewis hamilton","sebastian vettel","sergio perez","felipe massa","daniil kvyat","felipe nasr","pastor maldonado","max verstappen","fernando alonso","romain grosjean"],
        "Gran Premio de Estados Unidos": ["lewis hamilton","nico rosberg","sebastian vettel","max verstappen","sergio perez","jenson button","carlos sainz","pastor maldonado","felipe nasr","daniel ricciardo"],
        "Gran Premio de México": ["nico rosberg","lewis hamilton","valtteri bottas","daniil kvyat","daniel ricciardo","felipe massa","nico hulkenberg","sergio perez","max verstappen","romain grosjean"],
        "Gran Premio de Brasil": ["nico rosberg","lewis hamilton","sebastian vettel","kimi raikkonen","valtteri bottas","nico hulkenberg","daniil kvyat","romain grosjean","max verstappen","sergio perez"],
        "Gran Premio de Abu Dabi": ["nico rosberg","lewis hamilton","kimi raikkonen","sebastian vettel","sergio perez","daniel ricciardo","nico hulkenberg","felipe massa","romain grosjean","daniil kvyat"]
    },
    2016: {
        "Gran Premio de Australia": ["nico rosberg","lewis hamilton","sebastian vettel","daniel ricciardo","felipe massa","romain grosjean","nico hulkenberg","valtteri bottas","carlos sainz","max verstappen"],
        "Gran Premio de Bahréin": ["nico rosberg","kimi raikkonen","lewis hamilton","daniel ricciardo","romain grosjean","max verstappen","daniil kvyat","felipe massa","valtteri bottas","stoffel vandoorne"],
        "Gran Premio de China": ["nico rosberg","sebastian vettel","daniil kvyat","daniel ricciardo","kimi raikkonen","felipe massa","max verstappen","carlos sainz","valtteri bottas","sergio perez"],
        "Gran Premio de Rusia": ["nico rosberg","lewis hamilton","kimi raikkonen","valtteri bottas","felipe massa","fernando alonso","kevin magnussen","romain grosjean","sergio perez","jenson button"],
        "Gran Premio de España": ["max verstappen","kimi raikkonen","sebastian vettel","daniel ricciardo","valtteri bottas","carlos sainz","sergio perez","felipe massa","jenson button","daniil kvyat"],
        "Gran Premio de Mónaco": ["lewis hamilton","daniel ricciardo","sergio perez","sebastian vettel","fernando alonso","nico hulkenberg","nico rosberg","carlos sainz","jenson button","felipe massa"],
        "Gran Premio de Canadá": ["lewis hamilton","sebastian vettel","valtteri bottas","max verstappen","nico rosberg","kimi raikkonen","daniel ricciardo","nico hulkenberg","carlos sainz","sergio perez"],
        "Gran Premio de Azerbaiyán": ["nico rosberg","sebastian vettel","sergio perez","kimi raikkonen","lewis hamilton","valtteri bottas","daniel ricciardo","max verstappen","nico hulkenberg","felipe massa"],
        "Gran Premio de Austria": ["lewis hamilton","max verstappen","kimi raikkonen","daniel ricciardo","jenson button","romain grosjean","carlos sainz","valtteri bottas","pascal wehrlein","esteban gutierrez"],
        "Gran Premio de Gran Bretaña": ["lewis hamilton","nico rosberg","max verstappen","daniel ricciardo","kimi raikkonen","sergio perez","nico hulkenberg","carlos sainz","sebastian vettel","daniil kvyat"],
        "Gran Premio de Hungría": ["lewis hamilton","nico rosberg","daniel ricciardo","sebastian vettel","max verstappen","kimi raikkonen","fernando alonso","carlos sainz","valtteri bottas","nico hulkenberg"],
        "Gran Premio de Alemania": ["lewis hamilton","daniel ricciardo","max verstappen","nico rosberg","sebastian vettel","kimi raikkonen","nico hulkenberg","jenson button","valtteri bottas","sergio perez"],
        "Gran Premio de Bélgica": ["nico rosberg","daniel ricciardo","lewis hamilton","nico hulkenberg","sergio perez","sebastian vettel","fernando alonso","valtteri bottas","kimi raikkonen","felipe massa"],
        "Gran Premio de Italia": ["nico rosberg","lewis hamilton","sebastian vettel","kimi raikkonen","daniel ricciardo","valtteri bottas","max verstappen","sergio perez","felipe massa","nico hulkenberg"],
        "Gran Premio de Singapur": ["nico rosberg","daniel ricciardo","lewis hamilton","kimi raikkonen","sebastian vettel","max verstappen","fernando alonso","sergio perez","daniil kvyat","kevin magnussen"],
        "Gran Premio de Malasia": ["daniel ricciardo","max verstappen","nico rosberg","sebastian vettel","sergio perez","fernando alonso","nico hulkenberg","jenson button","valtteri bottas","felipe massa"],
        "Gran Premio de Japón": ["nico rosberg","max verstappen","lewis hamilton","daniel ricciardo","sebastian vettel","sergio perez","romain grosjean","felipe massa","carlos sainz","daniil kvyat"],
        "Gran Premio de Estados Unidos": ["lewis hamilton","nico rosberg","daniel ricciardo","sebastian vettel","fernando alonso","carlos sainz","felipe massa","sergio perez","jenson button","romain grosjean"],
        "Gran Premio de México": ["lewis hamilton","nico rosberg","max verstappen","sebastian vettel","daniel ricciardo","kimi raikkonen","nico hulkenberg","valtteri bottas","felipe massa","sergio perez"],
        "Gran Premio de Brasil": ["lewis hamilton","nico rosberg","max verstappen","sergio perez","sebastian vettel","carlos sainz","nico hulkenberg","daniel ricciardo","felipe massa","fernando alonso"],
        "Gran Premio de Abu Dabi": ["lewis hamilton","nico rosberg","sebastian vettel","max verstappen","daniel ricciardo","kimi raikkonen","nico hulkenberg","sergio perez","felipe massa","fernando alonso"],
    },
    2017: {
        "Gran Premio de Australia": ["sebastian vettel","lewis hamilton","valtteri bottas","kimi raikkonen","max verstappen","felipe massa","sergio perez","carlos sainz","daniil kvyat","esteban ocon"],
        "Gran Premio de China": ["lewis hamilton","sebastian vettel","max verstappen","daniel ricciardo","kimi raikkonen","valtteri bottas","carlos sainz","kevin magnussen","sergio perez","esteban ocon"],
        "Gran Premio de Bahréin": ["sebastian vettel","lewis hamilton","valtteri bottas","kimi raikkonen","daniel ricciardo","felipe massa","sergio perez","romain grosjean","nico hulkenberg","esteban ocon"],
        "Gran Premio de Rusia": ["valtteri bottas","sebastian vettel","kimi raikkonen","lewis hamilton","max verstappen","sergio perez","esteban ocon","nico hulkenberg","felipe massa","carlos sainz"],
        "Gran Premio de España": ["lewis hamilton","sebastian vettel","daniel ricciardo","sergio perez","esteban ocon","nico hulkenberg","carlos sainz","pascal wehrlein","daniil kvyat","romain grosjean"],
        "Gran Premio de Mónaco": ["sebastian vettel","kimi raikkonen","daniel ricciardo","valtteri bottas","max verstappen","carlos sainz","lewis hamilton","romain grosjean","felipe massa","kevin magnussen"],
        "Gran Premio de Canadá": ["lewis hamilton","valtteri bottas","daniel ricciardo","sebastian vettel","sergio perez","esteban ocon","nico hulkenberg","lance stroll","max verstappen","carlos sainz"],
        "Gran Premio de Azerbaiyán": ["daniel ricciardo","valtteri bottas","lance stroll","sebastian vettel","lewis hamilton","esteban ocon","kevin magnussen","carlos sainz","fernando alonso","pascal wehrlein"],
        "Gran Premio de Austria": ["valtteri bottas","sebastian vettel","daniel ricciardo","lewis hamilton","kimi raikkonen","romain grosjean","sergio perez","esteban ocon","felipe massa","lance stroll"],
        "Gran Premio de Gran Bretaña": ["lewis hamilton","valtteri bottas","kimi raikkonen","max verstappen","daniel ricciardo","nico hulkenberg","esteban ocon","sergio perez","felipe massa","sebastian vettel"],
        "Gran Premio de Hungría": ["sebastian vettel","kimi raikkonen","valtteri bottas","lewis hamilton","max verstappen","fernando alonso","carlos sainz","sergio perez","esteban ocon","stoffel vandoorne"],
        "Gran Premio de Bélgica": ["lewis hamilton","sebastian vettel","daniel ricciardo","kimi raikkonen","valtteri bottas","nico hulkenberg","romain grosjean","felipe massa","esteban ocon","carlos sainz"],
        "Gran Premio de Italia": ["lewis hamilton","valtteri bottas","sebastian vettel","daniel ricciardo","kimi raikkonen","esteban ocon","lance stroll","felipe massa","sergio perez","max verstappen"],
        "Gran Premio de Singapur": ["lewis hamilton","daniel ricciardo","valtteri bottas","kimi raikkonen","sebastian vettel","stoffel vandoorne","nico hulkenberg","carlos sainz","sergio perez","esteban ocon"],
        "Gran Premio de Malasia": ["max verstappen","lewis hamilton","daniel ricciardo","sebastian vettel","valtteri bottas","sergio perez","stoffel vandoorne","lance stroll","felipe massa","esteban ocon"],
        "Gran Premio de Japón": ["lewis hamilton","max verstappen","daniel ricciardo","valtteri bottas","kimi raikkonen","esteban ocon","sergio perez","kevin magnussen","romain grosjean","felipe massa"],
        "Gran Premio de Estados Unidos": ["lewis hamilton","sebastian vettel","kimi raikkonen","max verstappen","valtteri bottas","esteban ocon","carlos sainz","sergio perez","felipe massa","daniil kvyat"],
        "Gran Premio de México": ["max verstappen","valtteri bottas","kimi raikkonen","sebastian vettel","esteban ocon","lance stroll","sergio perez","kevin magnussen","lewis hamilton","fernando alonso"],
        "Gran Premio de Brasil": ["sebastian vettel","valtteri bottas","kimi raikkonen","lewis hamilton","max verstappen","daniel ricciardo","felipe massa","fernando alonso","sergio perez","nico hulkenberg"],
        "Gran Premio de Abu Dabi": ["valtteri bottas","lewis hamilton","sebastian vettel","kimi raikkonen","max verstappen","nico hulkenberg","sergio perez","esteban ocon","fernando alonso","felipe massa"],
    },
    2018: {
        "Gran Premio de Australia": ["sebastian vettel","lewis hamilton","kimi raikkonen","daniel ricciardo","fernando alonso","max verstappen","nico hulkenberg","valtteri bottas","stoffel vandoorne","carlos sainz"],
        "Gran Premio de Bahréin": ["sebastian vettel","valtteri bottas","lewis hamilton","pierre gasly","kevin magnussen","nico hulkenberg","fernando alonso","stoffel vandoorne","marcus ericsson","esteban ocon"],
        "Gran Premio de China": ["daniel ricciardo","valtteri bottas","kimi raikkonen","lewis hamilton","max verstappen","nico hulkenberg","fernando alonso","sebastian vettel","carlos sainz","kevin magnussen"],
        "Gran Premio de Azerbaiyán": ["lewis hamilton","kimi raikkonen","sergio perez","sebastian vettel","carlos sainz","charles leclerc","fernando alonso","lance stroll","stoffel vandoorne","brendon hartley"],
        "Gran Premio de España": ["lewis hamilton","valtteri bottas","max verstappen","sebastian vettel","daniel ricciardo","kevin magnussen","carlos sainz","fernando alonso","sergio perez","charles leclerc"],
        "Gran Premio de Mónaco": ["daniel ricciardo","sebastian vettel","lewis hamilton","kimi raikkonen","valtteri bottas","esteban ocon","pierre gasly","nico hulkenberg","max verstappen","carlos sainz"],
        "Gran Premio de Canadá": ["sebastian vettel","valtteri bottas","max verstappen","daniel ricciardo","lewis hamilton","kimi raikkonen","nico hulkenberg","carlos sainz","esteban ocon","charles leclerc"],
        "Gran Premio de Francia": ["lewis hamilton","max verstappen","kimi raikkonen","daniel ricciardo","sebastian vettel","kevin magnussen","valtteri bottas","carlos sainz","nico hulkenberg","charles leclerc"],
        "Gran Premio de Austria": ["max verstappen","kimi raikkonen","sebastian vettel","romain grosjean","kevin magnussen","esteban ocon","sergio perez","fernando alonso","charles leclerc","marcus ericsson"],
        "Gran Premio de Gran Bretaña": ["sebastian vettel","lewis hamilton","kimi raikkonen","valtteri bottas","daniel ricciardo","nico hulkenberg","esteban ocon","fernando alonso","kevin magnussen","pierre gasly"],
        "Gran Premio de Alemania": ["lewis hamilton","valtteri bottas","kimi raikkonen","max verstappen","nico hulkenberg","romain grosjean","sergio perez","esteban ocon","marcus ericsson","brendon hartley"],
        "Gran Premio de Hungría": ["lewis hamilton","sebastian vettel","kimi raikkonen","daniel ricciardo","valtteri bottas","pierre gasly","kevin magnussen","fernando alonso","carlos sainz","romain grosjean"],
        "Gran Premio de Bélgica": ["sebastian vettel","lewis hamilton","max verstappen","valtteri bottas","sergio perez","esteban ocon","romain grosjean","kevin magnussen","pierre gasly","marcus ericsson"],
        "Gran Premio de Italia": ["lewis hamilton","kimi raikkonen","valtteri bottas","sebastian vettel","max verstappen","romain grosjean","esteban ocon","sergio perez","carlos sainz","lance stroll"],
        "Gran Premio de Singapur": ["lewis hamilton","max verstappen","sebastian vettel","valtteri bottas","kimi raikkonen","daniel ricciardo","fernando alonso","carlos sainz","charles leclerc","nico hulkenberg"],
        "Gran Premio de Rusia": ["lewis hamilton","valtteri bottas","sebastian vettel","kimi raikkonen","max verstappen","daniel ricciardo","charles leclerc","kevin magnussen","esteban ocon","sergio perez"],
        "Gran Premio de Japón": ["lewis hamilton","valtteri bottas","max verstappen","daniel ricciardo","kimi raikkonen","sebastian vettel","sergio perez","romain grosjean","esteban ocon","carlos sainz"],
        "Gran Premio de Estados Unidos": ["kimi raikkonen","max verstappen","lewis hamilton","daniel ricciardo","valtteri bottas","nico hulkenberg","carlos sainz","esteban ocon","kevin magnussen","sergio perez"],
        "Gran Premio de México": ["max verstappen","sebastian vettel","kimi raikkonen","lewis hamilton","valtteri bottas","nico hulkenberg","charles leclerc","stoffel vandoorne","marcus ericsson","pierre gasly"],
        "Gran Premio de Brasil": ["lewis hamilton","max verstappen","kimi raikkonen","daniel ricciardo","valtteri bottas","sebastian vettel","charles leclerc","romain grosjean","kevin magnussen","sergio perez"],
        "Gran Premio de Abu Dabi": ["lewis hamilton","sebastian vettel","max verstappen","daniel ricciardo","valtteri bottas","carlos sainz","charles leclerc","sergio perez","romain grosjean","kevin magnussen"],
    },
    2019: {
        "Gran Premio de Australia": ["valtteri bottas","lewis hamilton","max verstappen","sebastian vettel","charles leclerc","kevin magnussen","nico hulkenberg","kimi raikkonen","lance stroll","daniil kvyat"],
        "Gran Premio de Bahréin": ["lewis hamilton","valtteri bottas","charles leclerc","max verstappen","sebastian vettel","lando norris","kimi raikkonen","pierre gasly","alexander albon","sergio perez"],
        "Gran Premio de China": ["lewis hamilton","valtteri bottas","sebastian vettel","max verstappen","charles leclerc","pierre gasly","daniel ricciardo","sergio perez","kimi raikkonen","alexander albon"],
        "Gran Premio de Azerbaiyán": ["valtteri bottas","lewis hamilton","sebastian vettel","max verstappen","charles leclerc","sergio perez","carlos sainz","lando norris","lance stroll","kimi raikkonen"],
        "Gran Premio de España": ["lewis hamilton","valtteri bottas","max verstappen","sebastian vettel","charles leclerc","pierre gasly","kevin magnussen","carlos sainz","daniil kvyat","romain grosjean"],
        "Gran Premio de Mónaco": ["lewis hamilton","sebastian vettel","valtteri bottas","max verstappen","pierre gasly","carlos sainz","daniil kvyat","alexander albon","daniel ricciardo","romain grosjean"],
        "Gran Premio de Canadá": ["lewis hamilton","sebastian vettel","charles leclerc","valtteri bottas","max verstappen","daniel ricciardo","nico hulkenberg","carlos sainz","sergio perez","lance stroll"],
        "Gran Premio de Francia": ["lewis hamilton","valtteri bottas","charles leclerc","max verstappen","sebastian vettel","carlos sainz","daniel ricciardo","pierre gasly","kimi raikkonen","nico hulkenberg"],
        "Gran Premio de Austria": ["max verstappen","charles leclerc","valtteri bottas","sebastian vettel","lewis hamilton","lando norris","pierre gasly","carlos sainz","kimi raikkonen","antonio giovinazzi"],
        "Gran Premio de Gran Bretaña": ["lewis hamilton","valtteri bottas","charles leclerc","pierre gasly","max verstappen","carlos sainz","daniel ricciardo","kimi raikkonen","daniil kvyat","nico hulkenberg"],
        "Gran Premio de Alemania": ["max verstappen","sebastian vettel","daniil kvyat","lance stroll","carlos sainz","alexander albon","kimi raikkonen","antonio giovinazzi","romain grosjean","kevin magnussen"],
        "Gran Premio de Hungría": ["lewis hamilton","max verstappen","sebastian vettel","charles leclerc","carlos sainz","pierre gasly","kimi raikkonen","valtteri bottas","lando norris","alexander albon"],
        "Gran Premio de Bélgica": ["charles leclerc","lewis hamilton","valtteri bottas","sebastian vettel","alexander albon","sergio perez","daniil kvyat","nico hulkenberg","pierre gasly","lance stroll"],
        "Gran Premio de Italia": ["charles leclerc","valtteri bottas","lewis hamilton","daniel ricciardo","nico hulkenberg","alexander albon","sergio perez","max verstappen","antonio giovinazzi","lando norris"],
        "Gran Premio de Singapur": ["sebastian vettel","charles leclerc","max verstappen","lewis hamilton","valtteri bottas","alexander albon","lando norris","pierre gasly","nico hulkenberg","antonio giovinazzi"],
        "Gran Premio de Rusia": ["lewis hamilton","valtteri bottas","charles leclerc","max verstappen","alexander albon","carlos sainz","sergio perez","lando norris","kevin magnussen","nico hulkenberg"],
        "Gran Premio de Japón": ["valtteri bottas","sebastian vettel","lewis hamilton","alexander albon","carlos sainz","charles leclerc","daniel ricciardo","pierre gasly","sergio perez","nico hulkenberg"],
        "Gran Premio de México": ["lewis hamilton","sebastian vettel","valtteri bottas","charles leclerc","alexander albon","max verstappen","sergio perez","daniel ricciardo","daniil kvyat","pierre gasly"],
        "Gran Premio de Estados Unidos": ["valtteri bottas","lewis hamilton","max verstappen","charles leclerc","alexander albon","daniel ricciardo","lando norris","carlos sainz","nico hulkenberg","sergio perez"],
        "Gran Premio de Brasil": ["max verstappen","pierre gasly","carlos sainz","lewis hamilton","charles leclerc","alexander albon","valtteri bottas","sebastian vettel","lando norris","sergio perez"],
        "Gran Premio de Abu Dabi": ["lewis hamilton","max verstappen","charles leclerc","valtteri bottas","sebastian vettel","alexander albon","sergio perez","lando norris","daniil kvyat","carlos sainz"]
    },
    2020: {
        "Gran Premio de Austria":         ["valtteri bottas","charles leclerc","lando norris","sebastian vettel","lance stroll","carlos sainz","esteban ocon","antonio giovinazzi","kimi raikkonen","george russell"],
        "Gran Premio de Estiria":         ["lewis hamilton","valtteri bottas","carlos sainz","sergio perez","sebastian vettel","lance stroll","charles leclerc","lando norris","george russell","pierre gasly"],
        "Gran Premio de Hungría":         ["lewis hamilton","max verstappen","valtteri bottas","lance stroll","alex albon","lando norris","daniel ricciardo","esteban ocon","pierre gasly","sebastian vettel"],
        "Gran Premio de Gran Bretaña":    ["lewis hamilton","max verstappen","valtteri bottas","charles leclerc","sebastian vettel","carlos sainz","lance stroll","lando norris","pierre gasly","esteban ocon"],
        "Gran Premio de 70 Aniversario":  ["max verstappen","valtteri bottas","lewis hamilton","lance stroll","carlos sainz","lando norris","alex albon","esteban ocon","fernando alonso","sebastian vettel"],
        "Gran Premio de España":          ["lewis hamilton","max verstappen","valtteri bottas","lance stroll","sergio perez","sebastian vettel","alex albon","pierre gasly","esteban ocon","daniel ricciardo"],
        "Gran Premio de Bélgica":         ["lewis hamilton","valtteri bottas","max verstappen","daniel ricciardo","nico hulkenberg","lance stroll","sergio perez","esteban ocon","pierre gasly","alex albon"],
        "Gran Premio de Italia":          ["pierre gasly","carlos sainz","lance stroll","lando norris","sebastian vettel","esteban ocon","nicholas latifi","antonio giovinazzi","kimi raikkonen","george russell"],
        "Gran Premio de Toscana":         ["lewis hamilton","valtteri bottas","alex albon","daniel ricciardo","lando norris","pierre gasly","lance stroll","esteban ocon","kimi raikkonen","sebastian vettel"],
        "Gran Premio de Rusia":           ["valtteri bottas","max verstappen","lewis hamilton","charles leclerc","lando norris","carlos sainz","pierre gasly","lance stroll","esteban ocon","daniel ricciardo"],
        "Gran Premio de Eifel":           ["lewis hamilton","max verstappen","daniel ricciardo","alex albon","daniil kvyat","sergio perez","lance stroll","lando norris","esteban ocon","kimi raikkonen"],
        "Gran Premio de Portugal":        ["lewis hamilton","valtteri bottas","max verstappen","carlos sainz","charles leclerc","lando norris","pierre gasly","esteban ocon","sebastian vettel","nicholas latifi"],
        "Gran Premio de Emilia-Romaña":   ["lewis hamilton","valtteri bottas","daniel ricciardo","max verstappen","charles leclerc","carlos sainz","alex albon","sebastian vettel","sergio perez","lando norris"],
        "Gran Premio de Turquía":         ["sergio perez","sebastian vettel","charles leclerc","lando norris","max verstappen","pierre gasly","lance stroll","antonio giovinazzi","valtteri bottas","esteban ocon"],
        "Gran Premio de Bahréin":         ["lewis hamilton","max verstappen","alex albon","lando norris","charles leclerc","pierre gasly","lance stroll","esteban ocon","sebastian vettel","daniil kvyat"],
        "Gran Premio de Sakhir":          ["sergio perez","esteban ocon","lance stroll","carlos sainz","lando norris","george russell","daniil kvyat","antonio giovinazzi","daniel ricciardo","pierre gasly"],
        "Gran Premio de Abu Dabi":        ["max verstappen","valtteri bottas","lewis hamilton","carlos sainz","esteban ocon","lance stroll","sebastian vettel","lando norris","charles leclerc","daniel ricciardo"],
    },
    2021: {
        "Gran Premio de Bahréin":         ["lewis hamilton","max verstappen","valtteri bottas","lando norris","sergio perez","charles leclerc","daniel ricciardo","carlos sainz","sebastian vettel","lance stroll"],
        "Gran Premio de Emilia-Romaña":   ["max verstappen","lewis hamilton","lando norris","valtteri bottas","charles leclerc","sebastian vettel","daniel ricciardo","carlos sainz","yuki tsunoda","george russell"],
        "Gran Premio de Portugal":        ["lewis hamilton","max verstappen","valtteri bottas","pierre gasly","sebastian vettel","lance stroll","sergio perez","lando norris","esteban ocon","daniel ricciardo"],
        "Gran Premio de España":          ["lewis hamilton","max verstappen","valtteri bottas","carlos sainz","sebastian vettel","lance stroll","esteban ocon","lando norris","sergio perez","kimi raikkonen"],
        "Gran Premio de Mónaco":          ["max verstappen","carlos sainz","lando norris","sebastian vettel","pierre gasly","antonio giovinazzi","sergio perez","lance stroll","charles leclerc","mick schumacher"],
        "Gran Premio de Azerbaiyán":      ["sergio perez","sebastian vettel","pierre gasly","charles leclerc","lando norris","lance stroll","carlos sainz","yuki tsunoda","nikita mazepin","antonio giovinazzi"],
        "Gran Premio de Francia":         ["max verstappen","lewis hamilton","valtteri bottas","sergio perez","carlos sainz","lando norris","pierre gasly","esteban ocon","daniel ricciardo","antonio giovinazzi"],
        "Gran Premio de Estiria":         ["max verstappen","lewis hamilton","valtteri bottas","norman nato","carlos sainz","lance stroll","lando norris","nikita mazepin","sebastian vettel","george russell"],
        "Gran Premio de Austria":         ["max verstappen","valtteri bottas","lando norris","carlos sainz","lewis hamilton","fernando alonso","esteban ocon","pierre gasly","sebastian vettel","daniel ricciardo"],
        "Gran Premio de Gran Bretaña":    ["lewis hamilton","charles leclerc","valtteri bottas","max verstappen","fernando alonso","pierre gasly","carlos sainz","lando norris","sergio perez","sebastian vettel"],
        "Gran Premio de Hungría":         ["esteban ocon","lewis hamilton","carlos sainz","lando norris","valtteri bottas","george russell","nicolas latifi","lance stroll","max verstappen","yuki tsunoda"],
        "Gran Premio de Bélgica":         ["max verstappen","george russell","lewis hamilton","daniel ricciardo","sebastian vettel","valtteri bottas","lance stroll","esteban ocon","mick schumacher","nicholas latifi"],
        "Gran Premio de Países Bajos":    ["max verstappen","lewis hamilton","valtteri bottas","pierre gasly","carlos sainz","lando norris","charles leclerc","sebastian vettel","fernando alonso","lance stroll"],
        "Gran Premio de Italia":          ["daniel ricciardo","lando norris","valtteri bottas","charles leclerc","carlos sainz","sebastian vettel","lance stroll","fernando alonso","pierre gasly","esteban ocon"],
        "Gran Premio de Rusia":           ["lewis hamilton","max verstappen","carlos sainz","lando norris","valtteri bottas","sergio perez","pierre gasly","esteban ocon","lance stroll","yuki tsunoda"],
        "Gran Premio de Turquía":         ["valtteri bottas","max verstappen","sergio perez","charles leclerc","lando norris","sebastian vettel","pierre gasly","lance stroll","fernando alonso","esteban ocon"],
        "Gran Premio de Estados Unidos":  ["max verstappen","lewis hamilton","sergio perez","sebastian vettel","charles leclerc","daniel ricciardo","carlos sainz","yuki tsunoda","pierre gasly","lance stroll"],
        "Gran Premio de México":          ["max verstappen","lewis hamilton","sergio perez","pierre gasly","sebastian vettel","carlos sainz","lando norris","charles leclerc","valtteri bottas","yuki tsunoda"],
        "Gran Premio de Brasil":          ["lewis hamilton","max verstappen","valtteri bottas","pierre gasly","carlos sainz","lando norris","fernando alonso","esteban ocon","lance stroll","mick schumacher"],
        "Gran Premio de Catar":           ["lewis hamilton","max verstappen","fernando alonso","lando norris","sergio perez","esteban ocon","lance stroll","carlos sainz","pierre gasly","sebastian vettel"],
        "Gran Premio de Arabia Saudí":    ["lewis hamilton","max verstappen","valtteri bottas","esteban ocon","pierre gasly","sebastian vettel","carlos sainz","charles leclerc","nicholas latifi","lance stroll"],
        "Gran Premio de Abu Dabi":        ["max verstappen","lewis hamilton","carlos sainz","yuki tsunoda","valtteri bottas","pierre gasly","esteban ocon","lance stroll","sebastian vettel","lando norris"],
    },
    2022: {
        "Gran Premio de Bahréin":         ["charles leclerc","carlos sainz","lewis hamilton","george russell","valtteri bottas","esteban ocon","lando norris","sebastian vettel","yuki tsunoda","pierre gasly"],
        "Gran Premio de Arabia Saudí":    ["carlos sainz","max verstappen","carlos sainz","valtteri bottas","esteban ocon","lando norris","mick schumacher","sebastian vettel","pierre gasly","lance stroll"],
        "Gran Premio de Australia":       ["charles leclerc","sergio perez","george russell","lewis hamilton","sebastian vettel","lando norris","valtteri bottas","esteban ocon","lance stroll","sebastian vettel"],
        "Gran Premio de Emilia-Romaña":   ["max verstappen","pierre gasly","lando norris","valtteri bottas","sebastian vettel","yuki tsunoda","sebastian vettel","lance stroll","mick schumacher","esteban ocon"],
        "Gran Premio de Miami":           ["max verstappen","charles leclerc","carlos sainz","sergio perez","valtteri bottas","lance stroll","sebastian vettel","kevin magnussen","esteban ocon","lando norris"],
        "Gran Premio de España":          ["max verstappen","sergio perez","george russell","valtteri bottas","carlos sainz","esteban ocon","lance stroll","sebastian vettel","fernando alonso","mick schumacher"],
        "Gran Premio de Mónaco":          ["sergio perez","carlos sainz","max verstappen","charles leclerc","lando norris","sebastian vettel","george russell","lance stroll","esteban ocon","sebastian vettel"],
        "Gran Premio de Azerbaiyán":      ["max verstappen","sergio perez","george russell","sebastian vettel","nicholas latifi","lando norris","sebastian vettel","lance stroll","sebastian vettel","yuki tsunoda"],
        "Gran Premio de Canadá":          ["max verstappen","carlos sainz","lewis hamilton","george russell","esteban ocon","valtteri bottas","sebastian vettel","guanyu zhou","fernando alonso","lance stroll"],
        "Gran Premio de Gran Bretaña":    ["carlos sainz","sergio perez","lewis hamilton","fernando alonso","mick schumacher","sebastian vettel","kevin magnussen","valtteri bottas","lando norris","pierre gasly"],
        "Gran Premio de Austria":         ["charles leclerc","max verstappen","lewis hamilton","esteban ocon","mick schumacher","sebastian vettel","valtteri bottas","pierre gasly","lance stroll","sebastian vettel"],
        "Gran Premio de Francia":         ["max verstappen","lewis hamilton","george russell","sergio perez","sebastian vettel","fernando alonso","lando norris","esteban ocon","sebastian vettel","lance stroll"],
        "Gran Premio de Hungría":         ["max verstappen","george russell","lewis hamilton","carlos sainz","sergio perez","valtteri bottas","mick schumacher","sebastian vettel","sebastian vettel","lance stroll"],
        "Gran Premio de Bélgica":         ["max verstappen","sergio perez","carlos sainz","esteban ocon","sebastian vettel","fernando alonso","pierre gasly","sebastian vettel","lance stroll","valtteri bottas"],
        "Gran Premio de Países Bajos":    ["max verstappen","george russell","charles leclerc","lewis hamilton","fernando alonso","lando norris","valtteri bottas","sebastian vettel","pierre gasly","lance stroll"],
        "Gran Premio de Italia":          ["max verstappen","charles leclerc","george russell","daniel ricciardo","valtteri bottas","sebastian vettel","guanyu zhou","lance stroll","mick schumacher","pierre gasly"],
        "Gran Premio de Singapur":        ["sergio perez","charles leclerc","esteban ocon","lance stroll","sebastian vettel","max verstappen","george russell","nicholas latifi","lando norris","sebastian vettel"],
        "Gran Premio de Japón":           ["max verstappen","sebastian vettel","charles leclerc","esteban ocon","lance stroll","sebastian vettel","nicholas latifi","mick schumacher","sebastian vettel","pierre gasly"],
        "Gran Premio de Estados Unidos":  ["max verstappen","lewis hamilton","george russell","sebastian vettel","lando norris","lance stroll","mick schumacher","sebastian vettel","esteban ocon","pierre gasly"],
        "Gran Premio de México":          ["max verstappen","lewis hamilton","sergio perez","george russell","sebastian vettel","daniel ricciardo","esteban ocon","lance stroll","mick schumacher","valtteri bottas"],
        "Gran Premio de Brasil":          ["george russell","lewis hamilton","carlos sainz","fernando alonso","valtteri bottas","lance stroll","esteban ocon","sebastian vettel","pierre gasly","guanyu zhou"],
        "Gran Premio de Abu Dabi":        ["max verstappen","charles leclerc","sergio perez","carlos sainz","sebastian vettel","lance stroll","esteban ocon","lando norris","sebastian vettel","nicholas latifi"],
    },
    2023: {
        "Gran Premio de Bahréin":         ["max verstappen","sergio perez","fernando alonso","carlos sainz","lewis hamilton","lance stroll","george russell","valtteri bottas","lando norris","esteban ocon"],
        "Gran Premio de Arabia Saudí":    ["sergio perez","max verstappen","fernando alonso","george russell","lance stroll","carlos sainz","lewis hamilton","oscar piastri","valtteri bottas","esteban ocon"],
        "Gran Premio de Australia":       ["max verstappen","lewis hamilton","fernando alonso","carlos sainz","lance stroll","valtteri bottas","pierre gasly","oscar piastri","lando norris","esteban ocon"],
        "Gran Premio de Azerbaiyán":      ["sergio perez","max verstappen","lance stroll","charles leclerc","fernando alonso","george russell","carlos sainz","lewis hamilton","sebastian vettel","lando norris"],
        "Gran Premio de Miami":           ["max verstappen","fernando alonso","carlos sainz","george russell","lance stroll","valtteri bottas","esteban ocon","lewis hamilton","oscar piastri","lando norris"],
        "Gran Premio de Mónaco":          ["max verstappen","fernando alonso","esteban ocon","lewis hamilton","george russell","lance stroll","carlos sainz","charles leclerc","lando norris","guanyu zhou"],
        "Gran Premio de España":          ["max verstappen","lewis hamilton","george russell","lando norris","carlos sainz","sergio perez","lance stroll","esteban ocon","pierre gasly","oscar piastri"],
        "Gran Premio de Canadá":          ["max verstappen","fernando alonso","lance stroll","lewis hamilton","charles leclerc","carlos sainz","lando norris","sergio perez","esteban ocon","yuki tsunoda"],
        "Gran Premio de Austria":         ["max verstappen","charles leclerc","lando norris","oscar piastri","nico hulkenberg","lewis hamilton","sebastian vettel","carlos sainz","esteban ocon","george russell"],
        "Gran Premio de Gran Bretaña":    ["max verstappen","lando norris","lewis hamilton","oscar piastri","carlos sainz","fernando alonso","lance stroll","esteban ocon","alex albon","pierre gasly"],
        "Gran Premio de Hungría":         ["max verstappen","lando norris","sergio perez","lewis hamilton","lance stroll","carlos sainz","charles leclerc","george russell","oscar piastri","pierre gasly"],
        "Gran Premio de Bélgica":         ["max verstappen","sergio perez","lewis hamilton","fernando alonso","lance stroll","charles leclerc","carlos sainz","lando norris","esteban ocon","valtteri bottas"],
        "Gran Premio de Países Bajos":    ["max verstappen","fernando alonso","pierre gasly","charles leclerc","lance stroll","lando norris","oscar piastri","nico hulkenberg","lewis hamilton","george russell"],
        "Gran Premio de Italia":          ["max verstappen","carlos sainz","george russell","charles leclerc","lando norris","sergio perez","pierre gasly","alex albon","esteban ocon","lance stroll"],
        "Gran Premio de Singapur":        ["carlos sainz","lando norris","lewis hamilton","charles leclerc","max verstappen","sergio perez","lance stroll","oscar piastri","esteban ocon","pierre gasly"],
        "Gran Premio de Japón":           ["max verstappen","lando norris","oscar piastri","esteban ocon","lewis hamilton","lance stroll","carlos sainz","george russell","pierre gasly","nico hulkenberg"],
        "Gran Premio de Catar":           ["max verstappen","oscar piastri","lando norris","george russell","fernando alonso","esteban ocon","valtteri bottas","lance stroll","carlos sainz","pierre gasly"],
        "Gran Premio de Estados Unidos":  ["max verstappen","lando norris","carlos sainz","sergio perez","george russell","fernando alonso","lance stroll","esteban ocon","pierre gasly","nico hulkenberg"],
        "Gran Premio de México":          ["max verstappen","lewis hamilton","fernando alonso","lance stroll","carlos sainz","sergio perez","lando norris","pierre gasly","esteban ocon","yuki tsunoda"],
        "Gran Premio de Brasil":          ["max verstappen","lando norris","fernando alonso","lance stroll","esteban ocon","sergio perez","carlos sainz","pierre gasly","charles leclerc","guanyu zhou"],
        "Gran Premio de Las Vegas":       ["max verstappen","charles leclerc","sergio perez","esteban ocon","lance stroll","carlos sainz","lando norris","oscar piastri","pierre gasly","george russell"],
        "Gran Premio de Abu Dabi":        ["max verstappen","charles leclerc","george russell","oscar piastri","lance stroll","lando norris","carlos sainz","lewis hamilton","fernando alonso","pierre gasly"],
    },
    2024: {
        "Gran Premio de Bahréin":         ["max verstappen","carlos sainz","charles leclerc","oscar piastri","fernando alonso","lando norris","george russell","lewis hamilton","lance stroll","nico hulkenberg"],
        "Gran Premio de Arabia Saudí":    ["max verstappen","sergio perez","charles leclerc","oscar piastri","fernando alonso","lando norris","lance stroll","george russell","lewis hamilton","carlos sainz"],
        "Gran Premio de Australia":       ["carlos sainz","charles leclerc","lando norris","oscar piastri","george russell","fernando alonso","lance stroll","nico hulkenberg","lewis hamilton","kevin magnussen"],
        "Gran Premio de Japón":           ["max verstappen","sergio perez","carlos sainz","charles leclerc","george russell","lando norris","fernando alonso","lance stroll","nico hulkenberg","esteban ocon"],
        "Gran Premio de China":           ["max verstappen","lando norris","sergio perez","carlos sainz","oscar piastri","lewis hamilton","nico hulkenberg","george russell","fernando alonso","lance stroll"],
        "Gran Premio de Miami":           ["lando norris","max verstappen","charles leclerc","sergio perez","fernando alonso","carlos sainz","esteban ocon","george russell","pierre gasly","lance stroll"],
        "Gran Premio de Emilia-Romaña":   ["max verstappen","lando norris","charles leclerc","oscar piastri","sergio perez","george russell","carlos sainz","kevin magnussen","fernando alonso","lance stroll"],
        "Gran Premio de Mónaco":          ["charles leclerc","oscar piastri","carlos sainz","lando norris","max verstappen","george russell","fernando alonso","sergio perez","lance stroll","pierre gasly"],
        "Gran Premio de Canadá":          ["max verstappen","lando norris","george russell","lewis hamilton","oscar piastri","sergio perez","charles leclerc","carlos sainz","pierre gasly","nico hulkenberg"],
        "Gran Premio de España":          ["max verstappen","lando norris","lewis hamilton","george russell","fernando alonso","carlos sainz","sergio perez","charles leclerc","lance stroll","esteban ocon"],
        "Gran Premio de Austria":         ["george russell","max verstappen","lando norris","carlos sainz","lewis hamilton","oscar piastri","sergio perez","nico hulkenberg","lance stroll","esteban ocon"],
        "Gran Premio de Gran Bretaña":    ["lewis hamilton","max verstappen","carlos sainz","oscar piastri","lando norris","charles leclerc","sergio perez","nico hulkenberg","fernando alonso","lance stroll"],
        "Gran Premio de Hungría":         ["oscar piastri","lando norris","george russell","lewis hamilton","max verstappen","charles leclerc","carlos sainz","sergio perez","fernando alonso","lance stroll"],
        "Gran Premio de Bélgica":         ["lewis hamilton","oscar piastri","charles leclerc","sergio perez","pierre gasly","lando norris","carlos sainz","franco colapinto","nico hulkenberg","esteban ocon"],
        "Gran Premio de Países Bajos":    ["lando norris","max verstappen","charles leclerc","carlos sainz","george russell","oscar piastri","sergio perez","fernando alonso","lance stroll","esteban ocon"],
        "Gran Premio de Italia":          ["charles leclerc","oscar piastri","lando norris","carlos sainz","lewis hamilton","george russell","max verstappen","pierre gasly","esteban ocon","nico hulkenberg"],
        "Gran Premio de Azerbaiyán":      ["oscar piastri","charles leclerc","george russell","max verstappen","lando norris","carlos sainz","sergio perez","lewis hamilton","lance stroll","franco colapinto"],
        "Gran Premio de Singapur":        ["lando norris","max verstappen","charles leclerc","carlos sainz","george russell","oscar piastri","sergio perez","fernando alonso","lewis hamilton","nico hulkenberg"],
        "Gran Premio de Estados Unidos":  ["charles leclerc","carlos sainz","max verstappen","lando norris","george russell","oscar piastri","pierre gasly","lewis hamilton","franco colapinto","liam lawson"],
        "Gran Premio de México":          ["carlos sainz","lando norris","charles leclerc","oscar piastri","max verstappen","george russell","esteban ocon","lance stroll","nico hulkenberg","lewis hamilton"],
        "Gran Premio de Brasil":          ["max verstappen","esteban ocon","pierre gasly","nico hulkenberg","fernando alonso","lance stroll","oliver bearman","liam lawson","carlos sainz","franco colapinto"],
        "Gran Premio de Las Vegas":       ["carlos sainz","max verstappen","pierre gasly","lando norris","charles leclerc","oscar piastri","nico hulkenberg","george russell","fernando alonso","lewis hamilton"],
        "Gran Premio de Catar":           ["max verstappen","lando norris","oscar piastri","carlos sainz","sergio perez","lance stroll","nico hulkenberg","esteban ocon","pierre gasly","yuki tsunoda"],
        "Gran Premio de Abu Dabi":        ["lando norris","carlos sainz","charles leclerc","oscar piastri","george russell","max verstappen","lewis hamilton","fernando alonso","lance stroll","nico hulkenberg"],
    },

    # ── 2025 ────────────────────────────────────────────────────
    2025: {
        "Gran Premio de Australia":        ["lando norris","max verstappen","george russell","alex albon","kimi antonelli","lance stroll","nico hulkenberg","charles leclerc","oscar piastri","lewis hamilton"],
        "Gran Premio de China":            ["oscar piastri","lando norris","george russell","max verstappen","esteban ocon","kimi antonelli","alex albon","oliver bearman","lance stroll","carlos sainz"],
        "Gran Premio de Japón":            ["max verstappen","lando norris","oscar piastri","charles leclerc","george russell","kimi antonelli","lewis hamilton","isack hadjar","alex albon","oliver bearman"],
        "Gran Premio de Bahréin":          ["oscar piastri","george russell","lando norris","charles leclerc","lewis hamilton","max verstappen","pierre gasly","esteban ocon","yuki tsunoda","oliver bearman"],
        "Gran Premio de Arabia Saudí":     ["oscar piastri","max verstappen","charles leclerc","lando norris","george russell","kimi antonelli","lewis hamilton","carlos sainz","alex albon","isack hadjar"],
        "Gran Premio de Miami":            ["oscar piastri","lando norris","george russell","max verstappen","alex albon","kimi antonelli","charles leclerc","lewis hamilton","carlos sainz","yuki tsunoda"],
        "Gran Premio de Emilia-Romaña":    ["max verstappen","lando norris","oscar piastri","lewis hamilton","alex albon","charles leclerc","george russell","carlos sainz","isack hadjar","yuki tsunoda"],
        "Gran Premio de Mónaco":           ["lando norris","charles leclerc","oscar piastri","max verstappen","lewis hamilton","isack hadjar","esteban ocon","liam lawson","alex albon","carlos sainz"],
        "Gran Premio de España":           ["oscar piastri","lando norris","charles leclerc","george russell","nico hulkenberg","lewis hamilton","isack hadjar","pierre gasly","fernando alonso","max verstappen"],
        "Gran Premio de Canadá":           ["george russell","max verstappen","kimi antonelli","oscar piastri","charles leclerc","lewis hamilton","fernando alonso","nico hulkenberg","esteban ocon","carlos sainz"],
        "Gran Premio de Austria":          ["lando norris","oscar piastri","charles leclerc","lewis hamilton","george russell","liam lawson","fernando alonso","gabriel bortoleto","nico hulkenberg","esteban ocon"],
        "Gran Premio de Gran Bretaña":     ["lando norris","oscar piastri","nico hulkenberg","lewis hamilton","max verstappen","pierre gasly","lance stroll","alex albon","fernando alonso","george russell"],
        "Gran Premio de Bélgica":          ["oscar piastri","lando norris","charles leclerc","max verstappen","george russell","alex albon","lewis hamilton","liam lawson","gabriel bortoleto","pierre gasly"],
        "Gran Premio de Hungría":          ["lando norris","oscar piastri","george russell","charles leclerc","fernando alonso","gabriel bortoleto","lance stroll","liam lawson","max verstappen","kimi antonelli"],
        "Gran Premio de Países Bajos":     ["oscar piastri","max verstappen","isack hadjar","george russell","alex albon","oliver bearman","lance stroll","fernando alonso","yuki tsunoda","esteban ocon"],
        "Gran Premio de Italia":           ["max verstappen","lando norris","oscar piastri","charles leclerc","george russell","lewis hamilton","alex albon","gabriel bortoleto","kimi antonelli","isack hadjar"],
        "Gran Premio de Azerbaiyán":       ["max verstappen","george russell","carlos sainz","kimi antonelli","liam lawson","yuki tsunoda","lando norris","lewis hamilton","charles leclerc","isack hadjar"],
        "Gran Premio de Singapur":         ["george russell","max verstappen","lando norris","oscar piastri","kimi antonelli","charles leclerc","fernando alonso","lewis hamilton","oliver bearman","carlos sainz"],
        "Gran Premio de Estados Unidos":   ["max verstappen","lando norris","charles leclerc","lewis hamilton","oscar piastri","george russell","yuki tsunoda","nico hulkenberg","oliver bearman","fernando alonso"],
        "Gran Premio de México":           ["lando norris","charles leclerc","max verstappen","oliver bearman","oscar piastri","kimi antonelli","george russell","lewis hamilton","esteban ocon","gabriel bortoleto"],
        "Gran Premio de Brasil":           ["lando norris","kimi antonelli","max verstappen","george russell","oscar piastri","oliver bearman","liam lawson","isack hadjar","nico hulkenberg","pierre gasly"],
        "Gran Premio de Las Vegas":        ["max verstappen","george russell","kimi antonelli","charles leclerc","carlos sainz","isack hadjar","nico hulkenberg","lewis hamilton","esteban ocon","oliver bearman"],
        "Gran Premio de Catar":            ["max verstappen","oscar piastri","carlos sainz","lando norris","kimi antonelli","george russell","fernando alonso","charles leclerc","liam lawson","yuki tsunoda"],
        "Gran Premio de Abu Dabi":         ["max verstappen","oscar piastri","lando norris","charles leclerc","george russell","fernando alonso","esteban ocon","lewis hamilton","nico hulkenberg","lance stroll"],
    },

    # ── 2026 ────────────────────────────────────────────────────
    2026: {
        "Gran Premio de Australia":        ["george russell","kimi antonelli","charles leclerc","lewis hamilton","lando norris","max verstappen","oliver bearman","arvid lindblad","gabriel bortoleto","pierre gasly"],
    },
}

# Flat list of all F1 drivers (for autocomplete in PodiumGame)
_ALL_GP_DRIVERS = sorted({
    normalize(d)
    for year_data in GP_RESULTS.values()
    for results in year_data.values()
    for d in results
})


# ══════════════════════════════════════════════════════════════════
#  BASE DE DATOS — CONSTRUCTORES F1
#  Campos por equipo:
#  "nombre": {
#    "nac":      nacionalidad,
#    "epocas":   décadas activas (ej: [1950,1960,1970]),
#    "motores":  motores usados,
#    "titles":   campeonatos de constructores,
#    "wins":     victorias totales,
#    "circuitos_victoria": circuitos donde ganó al menos 1 vez,
#    "pilotos_campeon": pilotos que fueron campeones con este equipo,
#  }
# ══════════════════════════════════════════════════════════════════
RAW_CONSTRUCTORS = {
    "ferrari": {
        "nac": "italiana", "epocas": [1950,1960,1970,1980,1990,2000,2010,2020],
        "motores": ["ferrari"],
        "titles": 16, "wins": 243,
        "circuitos_victoria": ["monaco","monza","silverstone","spa","suzuka","barcelona","bahrain","abu dhabi","budapest","melbourne","shanghai","interlagos","mexico","baku","singapore","zandvoort","imola","portimao","jeddah","montreal","hockenheim","nurburgring","austria","istanbul","valencia"],
        "pilotos_campeon": ["juan manuel fangio","mike hawthorn","phil hill","john surtees","niki lauda","jody scheckter","michael schumacher","kimi raikkonen"],
    },
    "mercedes": {
        "nac": "alemana", "epocas": [1950,2010,2020],
        "motores": ["mercedes"],
        "titles": 8, "wins": 125,
        "circuitos_victoria": ["monaco","silverstone","spa","suzuka","barcelona","bahrain","abu dhabi","budapest","melbourne","shanghai","interlagos","mexico","baku","singapore","zandvoort","imola","portimao","jeddah","montreal","austria","istanbul","nurburgring","sochi","mugello","istanbul","eifel","70th anniversary","styria","sakhir","bahrain","las vegas","qatar"],
        "pilotos_campeon": ["lewis hamilton","nico rosberg"],
    },
    "red bull": {
        "nac": "austriaca", "epocas": [2000,2010,2020],
        "motores": ["renault","honda","rbpt"],
        "titles": 7, "wins": 120,
        "circuitos_victoria": ["monaco","monza","silverstone","spa","suzuka","barcelona","bahrain","abu dhabi","budapest","melbourne","shanghai","interlagos","mexico","baku","singapore","zandvoort","imola","portimao","jeddah","montreal","austria","istanbul","nurburgring","malaysia","china","japan","qatar","las vegas"],
        "pilotos_campeon": ["sebastian vettel","max verstappen"],
    },
    "mclaren": {
        "nac": "británica", "epocas": [1960,1970,1980,1990,2000,2010,2020],
        "motores": ["ford","cosworth","chevrolet","ford","tag","honda","ford","mercedes","renault","mercedes","mercedes"],
        "titles": 8, "wins": 183,
        "circuitos_victoria": ["monaco","monza","silverstone","spa","suzuka","barcelona","bahrain","abu dhabi","budapest","melbourne","shanghai","interlagos","mexico","baku","singapore","canada","austria","malaysia","japan","san marino","imola","portimao","jeddah","las vegas","miami","zandvoort","qatar","sao paulo","saudi arabia","australia"],
        "pilotos_campeon": ["emerson fittipaldi","james hunt","niki lauda","alain prost","ayrton senna","mika hakkinen","lewis hamilton"],
    },
    "williams": {
        "nac": "británica", "epocas": [1970,1980,1990,2000,2010,2020],
        "motores": ["ford","cosworth","ford","toyota","renault","bmw","toyota","renault","mercedes","mercedes"],
        "titles": 9, "wins": 114,
        "circuitos_victoria": ["monaco","monza","silverstone","spa","suzuka","barcelona","bahrain","abu dhabi","budapest","melbourne","interlagos","canada","austria","japan","san marino","imola","nurburgring","hockenheim","portugal","france","brazil"],
        "pilotos_campeon": ["alan jones","keke rosberg","nelson piquet","nigel mansell","alain prost","damon hill","jacques villeneuve"],
    },
    "renault": {
        "nac": "francesa", "epocas": [1970,1980,2000,2010,2020],
        "motores": ["renault"],
        "titles": 2, "wins": 35,
        "circuitos_victoria": ["monaco","spa","suzuka","barcelona","bahrain","budapest","malaysia","japan","san marino","imola","nurburgring","hockenheim","austria","france","australia","canada","malaysia","bahrain","china","turkey","singapore","australia"],
        "pilotos_campeon": ["fernando alonso"],
    },
    "alpine": {
        "nac": "francesa", "epocas": [2020],
        "motores": ["renault"],
        "titles": 0, "wins": 1,
        "circuitos_victoria": ["hungary"],
        "pilotos_campeon": [],
    },
    "lotus": {
        "nac": "británica", "epocas": [1950,1960,1970,1980],
        "motores": ["climax","ford","cosworth","renault"],
        "titles": 7, "wins": 79,
        "circuitos_victoria": ["monaco","monza","silverstone","spa","suzuka","france","germany","netherlands","south africa","canada","austria","argentina","brazil","usa","portugal"],
        "pilotos_campeon": ["jim clark","jochen rindt","emerson fittipaldi","mario andretti"],
    },
    "brabham": {
        "nac": "británica", "epocas": [1960,1970,1980],
        "motores": ["climax","repco","ford","alfa romeo","cosworth","bmw"],
        "titles": 4, "wins": 35,
        "circuitos_victoria": ["monaco","monza","silverstone","spa","france","germany","netherlands","south africa","canada","austria","argentina"],
        "pilotos_campeon": ["jack brabham","denny hulme","nelson piquet"],
    },
    "tyrrell": {
        "nac": "británica", "epocas": [1960,1970,1980,1990],
        "motores": ["ford","cosworth","renault","yamaha"],
        "titles": 3, "wins": 23,
        "circuitos_victoria": ["monaco","monza","silverstone","spa","france","germany","netherlands","south africa","canada","austria","argentina","usa"],
        "pilotos_campeon": ["jackie stewart"],
    },
    "benetton": {
        "nac": "británica", "epocas": [1980,1990,2000],
        "motores": ["bmw","ford","cosworth","renault","playlife"],
        "titles": 2, "wins": 27,
        "circuitos_victoria": ["monaco","monza","silverstone","spa","suzuka","barcelona","hungary","japan","portugal","australia","canada","belgium","france","germany","san marino"],
        "pilotos_campeon": ["michael schumacher"],
    },
    "alfa romeo": {
        "nac": "italiana", "epocas": [1950,2010,2020],
        "motores": ["alfa romeo","ferrari"],
        "titles": 2, "wins": 11,
        "circuitos_victoria": ["monaco","monza","silverstone","spa","france","germany","switzerland","belgium"],
        "pilotos_campeon": ["giuseppe farina","juan manuel fangio"],
    },
    "cooper": {
        "nac": "británica", "epocas": [1950,1960],
        "motores": ["climax","maserati"],
        "titles": 2, "wins": 16,
        "circuitos_victoria": ["monaco","monza","silverstone","spa","france","germany","netherlands","south africa","usa","argentina"],
        "pilotos_campeon": ["jack brabham","bruce mclaren"],
    },
    "brm": {
        "nac": "británica", "epocas": [1950,1960,1970],
        "motores": ["brm"],
        "titles": 1, "wins": 17,
        "circuitos_victoria": ["monaco","monza","silverstone","spa","france","germany","netherlands","south africa","usa"],
        "pilotos_campeon": ["graham hill"],
    },
    "matra": {
        "nac": "francesa", "epocas": [1960,1970],
        "motores": ["ford","cosworth","matra"],
        "titles": 1, "wins": 9,
        "circuitos_victoria": ["monaco","monza","silverstone","spa","france","germany","netherlands","south africa","usa","canada"],
        "pilotos_campeon": ["jackie stewart"],
    },
    "march": {
        "nac": "británica", "epocas": [1970,1980],
        "motores": ["ford","cosworth","alfa romeo"],
        "titles": 0, "wins": 3,
        "circuitos_victoria": ["silvertone","france","sweden"],
        "pilotos_campeon": [],
    },
    "hesketh": {
        "nac": "británica", "epocas": [1970],
        "motores": ["ford","cosworth"],
        "titles": 0, "wins": 1,
        "circuitos_victoria": ["netherlands"],
        "pilotos_campeon": [],
    },
    "wolf": {
        "nac": "canadiense", "epocas": [1970],
        "motores": ["ford","cosworth"],
        "titles": 0, "wins": 3,
        "circuitos_victoria": ["argentina","monaco","canada"],
        "pilotos_campeon": [],
    },
    "shadow": {
        "nac": "estadounidense", "epocas": [1970],
        "motores": ["ford","cosworth"],
        "titles": 0, "wins": 1,
        "circuitos_victoria": ["austria"],
        "pilotos_campeon": [],
    },
    "ligier": {
        "nac": "francesa", "epocas": [1970,1980,1990],
        "motores": ["matra","ford","cosworth","renault","lamborghini","mugen"],
        "titles": 0, "wins": 9,
        "circuitos_victoria": ["sweden","argentina","brazil","spain","long beach","monaco","austria","canada","netherlands"],
        "pilotos_campeon": [],
    },
    "arrows": {
        "nac": "británica", "epocas": [1970,1980,1990,2000],
        "motores": ["ford","cosworth","bmw","megatron","ford","hart","yamaha","arrows","supertec","asiatech"],
        "titles": 0, "wins": 0,
        "circuitos_victoria": [],
        "pilotos_campeon": [],
    },
    "minardi": {
        "nac": "italiana", "epocas": [1980,1990,2000],
        "motores": ["ford","motori moderni","lamborghini","ferrari","ford","cosworth","asiatech"],
        "titles": 0, "wins": 0,
        "circuitos_victoria": [],
        "pilotos_campeon": [],
    },
    "jordan": {
        "nac": "irlandesa", "epocas": [1990,2000],
        "motores": ["ford","cosworth","yamaha","peugeot","mugen","honda","ford","bridgestone"],
        "titles": 0, "wins": 4,
        "circuitos_victoria": ["spa","monza","nurburgring","brazil","hungary"],
        "pilotos_campeon": [],
    },
    "sauber": {
        "nac": "suiza", "epocas": [1990,2000,2010,2020],
        "motores": ["ilmor","mercedes","petronas","ferrari","bmw","ferrari","honda","ferrari"],
        "titles": 0, "wins": 1,
        "circuitos_victoria": ["canada"],
        "pilotos_campeon": [],
    },
    "bar": {
        "nac": "británica", "epocas": [1990,2000],
        "motores": ["supertec","honda"],
        "titles": 0, "wins": 0,
        "circuitos_victoria": [],
        "pilotos_campeon": [],
    },
    "honda": {
        "nac": "japonesa", "epocas": [1960,2000],
        "motores": ["honda"],
        "titles": 0, "wins": 3,
        "circuitos_victoria": ["mexico","italy","hungary"],
        "pilotos_campeon": [],
    },
    "brawn gp": {
        "nac": "británica", "epocas": [2000],
        "motores": ["mercedes"],
        "titles": 1, "wins": 8,
        "circuitos_victoria": ["bahrain","australia","monaco","turkey","silverstone","valencia","brazil","japan"],
        "pilotos_campeon": ["jenson button"],
    },
    "force india": {
        "nac": "india", "epocas": [2000,2010],
        "motores": ["ferrari","mercedes"],
        "titles": 0, "wins": 3,
        "circuitos_victoria": ["spa","bahrain","monza"],
        "pilotos_campeon": [],
    },
    "racing point": {
        "nac": "británica", "epocas": [2010,2020],
        "motores": ["mercedes"],
        "titles": 0, "wins": 1,
        "circuitos_victoria": ["sakhir"],
        "pilotos_campeon": [],
    },
    "aston martin": {
        "nac": "británica", "epocas": [2020],
        "motores": ["mercedes"],
        "titles": 0, "wins": 0,
        "circuitos_victoria": [],
        "pilotos_campeon": [],
    },
    "haas": {
        "nac": "estadounidense", "epocas": [2010,2020],
        "motores": ["ferrari"],
        "titles": 0, "wins": 0,
        "circuitos_victoria": [],
        "pilotos_campeon": [],
    },
    "toro rosso": {
        "nac": "italiana", "epocas": [2000,2010],
        "motores": ["cosworth","ferrari","renault","honda"],
        "titles": 0, "wins": 1,
        "circuitos_victoria": ["monza"],
        "pilotos_campeon": [],
    },
    "alphatauri": {
        "nac": "italiana", "epocas": [2010,2020],
        "motores": ["honda","renault"],
        "titles": 0, "wins": 2,
        "circuitos_victoria": ["monza","bahrain"],
        "pilotos_campeon": [],
    },
    "rb": {
        "nac": "italiana", "epocas": [2020],
        "motores": ["honda"],
        "titles": 0, "wins": 0,
        "circuitos_victoria": [],
        "pilotos_campeon": [],
    },
    "toyota": {
        "nac": "japonesa", "epocas": [2000,2010],
        "motores": ["toyota"],
        "titles": 0, "wins": 0,
        "circuitos_victoria": [],
        "pilotos_campeon": [],
    },
    "bmw sauber": {
        "nac": "alemana", "epocas": [2000],
        "motores": ["bmw"],
        "titles": 0, "wins": 1,
        "circuitos_victoria": ["canada"],
        "pilotos_campeon": [],
    },
    "super aguri": {
        "nac": "japonesa", "epocas": [2000],
        "motores": ["honda"],
        "titles": 0, "wins": 0,
        "circuitos_victoria": [],
        "pilotos_campeon": [],
    },
    "virgin": {
        "nac": "británica", "epocas": [2010],
        "motores": ["cosworth"],
        "titles": 0, "wins": 0,
        "circuitos_victoria": [],
        "pilotos_campeon": [],
    },
    "hrt": {
        "nac": "española", "epocas": [2010],
        "motores": ["cosworth"],
        "titles": 0, "wins": 0,
        "circuitos_victoria": [],
        "pilotos_campeon": [],
    },
    "caterham": {
        "nac": "británica", "epocas": [2010],
        "motores": ["renault"],
        "titles": 0, "wins": 0,
        "circuitos_victoria": [],
        "pilotos_campeon": [],
    },
    "marussia": {
        "nac": "británica", "epocas": [2010],
        "motores": ["cosworth","ferrari"],
        "titles": 0, "wins": 0,
        "circuitos_victoria": [],
        "pilotos_campeon": [],
    },
    "maserati": {
        "nac": "italiana", "epocas": [1950],
        "motores": ["maserati"],
        "titles": 1, "wins": 9,
        "circuitos_victoria": ["argentina","belgium","france","germany","monaco","italy","pescara","morocco"],
        "pilotos_campeon": ["juan manuel fangio"],
    },
    "vanwall": {
        "nac": "británica", "epocas": [1950],
        "motores": ["vanwall"],
        "titles": 1, "wins": 9,
        "circuitos_victoria": ["silverstone","aintree","pescara","monza","spa","nurburgring","casablanca","morocco","france"],
        "pilotos_campeon": [],
    },
    "lancia": {
        "nac": "italiana", "epocas": [1950],
        "motores": ["lancia"],
        "titles": 0, "wins": 0,
        "circuitos_victoria": [],
        "pilotos_campeon": [],
    },
    "benetton ford": {
        "nac": "británica", "epocas": [1990],
        "motores": ["ford"],
        "titles": 0, "wins": 0,
        "circuitos_victoria": [],
        "pilotos_campeon": [],
    },
    "stewart": {
        "nac": "británica", "epocas": [1990],
        "motores": ["ford"],
        "titles": 0, "wins": 1,
        "circuitos_victoria": ["monaco"],
        "pilotos_campeon": [],
    },
    "prost": {
        "nac": "francesa", "epocas": [1990,2000],
        "motores": ["mugen","peugeot","ferrari"],
        "titles": 0, "wins": 0,
        "circuitos_victoria": [],
        "pilotos_campeon": [],
    },
    "techeetah": {
        "nac": "francesa", "epocas": [2010,2020],
        "motores": ["renault"],
        "titles": 0, "wins": 0,
        "circuitos_victoria": [],
        "pilotos_campeon": [],
    },
    "williams bmw": {
        "nac": "británica", "epocas": [2000],
        "motores": ["bmw"],
        "titles": 0, "wins": 0,
        "circuitos_victoria": [],
        "pilotos_campeon": [],
    },
    "kick sauber": {
        "nac": "suiza", "epocas": [2020],
        "motores": ["ferrari"],
        "titles": 0, "wins": 0,
        "circuitos_victoria": [],
        "pilotos_campeon": [],
    },
    # ── Equipos históricos adicionales ───────────────────────────
    "eagle": {
        "nac": "estadounidense", "epocas": [1960],
        "motores": ["climax","weslake"],
        "titles": 0, "wins": 1,
        "circuitos_victoria": ["spa"],
        "pilotos_campeon": [],
    },
    "honda ra272": {
        "nac": "japonesa", "epocas": [1960],
        "motores": ["honda"],
        "titles": 0, "wins": 1,
        "circuitos_victoria": ["mexico"],
        "pilotos_campeon": [],
    },
    "parnelli": {
        "nac": "estadounidense", "epocas": [1970],
        "motores": ["ford","cosworth"],
        "titles": 0, "wins": 0,
        "circuitos_victoria": [],
        "pilotos_campeon": [],
    },
    "ensign": {
        "nac": "británica", "epocas": [1970,1980],
        "motores": ["ford","cosworth"],
        "titles": 0, "wins": 0,
        "circuitos_victoria": [],
        "pilotos_campeon": [],
    },
    "fittipaldi": {
        "nac": "brasileña", "epocas": [1970,1980],
        "motores": ["ford","cosworth"],
        "titles": 0, "wins": 0,
        "circuitos_victoria": [],
        "pilotos_campeon": [],
    },
    "osella": {
        "nac": "italiana", "epocas": [1980],
        "motores": ["ford","cosworth","alfa romeo"],
        "titles": 0, "wins": 0,
        "circuitos_victoria": [],
        "pilotos_campeon": [],
    },
    "ats": {
        "nac": "alemana", "epocas": [1970,1980],
        "motores": ["ford","cosworth","bmw"],
        "titles": 0, "wins": 0,
        "circuitos_victoria": [],
        "pilotos_campeon": [],
    },
    "lola": {
        "nac": "británica", "epocas": [1960,1970,1980,1990],
        "motores": ["climax","ford","cosworth","lamborghini","ferrari","ford"],
        "titles": 0, "wins": 0,
        "circuitos_victoria": [],
        "pilotos_campeon": [],
    },
    "pacific": {
        "nac": "británica", "epocas": [1990],
        "motores": ["ford","cosworth","ilmor"],
        "titles": 0, "wins": 0,
        "circuitos_victoria": [],
        "pilotos_campeon": [],
    },
    "simtek": {
        "nac": "británica", "epocas": [1990],
        "motores": ["ford","cosworth"],
        "titles": 0, "wins": 0,
        "circuitos_victoria": [],
        "pilotos_campeon": [],
    },
    "footwork": {
        "nac": "británica", "epocas": [1990],
        "motores": ["ford","cosworth","hart","yamaha"],
        "titles": 0, "wins": 0,
        "circuitos_victoria": [],
        "pilotos_campeon": [],
    },
    "dallara": {
        "nac": "italiana", "epocas": [1990],
        "motores": ["ford","cosworth"],
        "titles": 0, "wins": 0,
        "circuitos_victoria": [],
        "pilotos_campeon": [],
    },
    "spyker": {
        "nac": "neerlandesa", "epocas": [2000],
        "motores": ["ferrari","honda"],
        "titles": 0, "wins": 0,
        "circuitos_victoria": [],
        "pilotos_campeon": [],
    },
    "midland": {
        "nac": "británica", "epocas": [2000],
        "motores": ["toyota"],
        "titles": 0, "wins": 0,
        "circuitos_victoria": [],
        "pilotos_campeon": [],
    },
    "aguri": {
        "nac": "japonesa", "epocas": [2000],
        "motores": ["honda"],
        "titles": 0, "wins": 0,
        "circuitos_victoria": [],
        "pilotos_campeon": [],
    },
    "manor": {
        "nac": "británica", "epocas": [2010],
        "motores": ["ferrari","mercedes"],
        "titles": 0, "wins": 0,
        "circuitos_victoria": [],
        "pilotos_campeon": [],
    },
}

def _build_constructor_categories():
    """Genera todas las categorías jugables para el Constructor Challenge."""
    cats = []

    NAC_FLAGS = {
        "italiana":"🇮🇹","alemana":"🇩🇪","británica":"🇬🇧","francesa":"🇫🇷",
        "austriaca":"🇦🇹","japonesa":"🇯🇵","estadounidense":"🇺🇸","suiza":"🇨🇭",
        "india":"🇮🇳","irlandesa":"🇮🇪","canadiense":"🇨🇦","española":"🇪🇸",
        "brasileña":"🇧🇷","neerlandesa":"🇳🇱",
    }
    MOTOR_FLAGS = {
        "ferrari":"🔴","mercedes":"⭐","renault":"🟡","honda":"🔵",
        "ford":"🔧","cosworth":"🔩","bmw":"⚪","tag":"🏷️",
    }

    # 1. Nacionalidad
    nacs = set(v["nac"] for v in RAW_CONSTRUCTORS.values())
    for nac in sorted(nacs):
        flag = NAC_FLAGS.get(nac, "🏁")
        teams = [t for t, v in RAW_CONSTRUCTORS.items() if v["nac"] == nac]
        if len(teams) >= 1:
            cats.append({
                "key":   f"nac:{nac}",
                "label": f"{flag} {nac.capitalize()}",
                "check": lambda t, _n=nac: RAW_CONSTRUCTORS[t]["nac"] == _n,
                "teams": teams,
            })

    # 2. Época
    EPOCAS = {
        1950: "Años 50s", 1960: "Años 60s", 1970: "Años 70s",
        1980: "Años 80s", 1990: "Años 90s", 2000: "Años 2000s",
        2010: "Años 2010s", 2020: "Años 2020s",
    }
    for dec, lbl in EPOCAS.items():
        teams = [t for t, v in RAW_CONSTRUCTORS.items() if dec in v["epocas"]]
        if len(teams) >= 1:
            cats.append({
                "key":   f"epoca:{dec}",
                "label": f"🗓️ {lbl}",
                "check": lambda t, _d=dec: _d in RAW_CONSTRUCTORS[t]["epocas"],
                "teams": teams,
            })

    # 3. Motor
    all_motors = set(m for v in RAW_CONSTRUCTORS.values() for m in v["motores"])
    for motor in sorted(all_motors):
        teams = [t for t, v in RAW_CONSTRUCTORS.items() if motor in v["motores"]]
        if len(teams) >= 2:
            flag = MOTOR_FLAGS.get(motor, "⚙️")
            cats.append({
                "key":   f"motor:{motor}",
                "label": f"{flag} Motor {motor.capitalize()}",
                "check": lambda t, _m=motor: _m in RAW_CONSTRUCTORS[t]["motores"],
                "teams": teams,
            })

    # 4. Logros
    cats.append({
        "key": "logro:campeon", "label": "👑 Ganó Campeonato",
        "check": lambda t: RAW_CONSTRUCTORS[t]["titles"] >= 1,
        "teams": [t for t, v in RAW_CONSTRUCTORS.items() if v["titles"] >= 1],
    })
    cats.append({
        "key": "logro:5titles", "label": "👑👑 ≥5 Campeonatos",
        "check": lambda t: RAW_CONSTRUCTORS[t]["titles"] >= 5,
        "teams": [t for t, v in RAW_CONSTRUCTORS.items() if v["titles"] >= 5],
    })
    cats.append({
        "key": "logro:wins1", "label": "🏆 Al menos 1 victoria",
        "check": lambda t: RAW_CONSTRUCTORS[t]["wins"] >= 1,
        "teams": [t for t, v in RAW_CONSTRUCTORS.items() if v["wins"] >= 1],
    })
    cats.append({
        "key": "logro:wins10", "label": "🏆🏆 ≥10 victorias",
        "check": lambda t: RAW_CONSTRUCTORS[t]["wins"] >= 10,
        "teams": [t for t, v in RAW_CONSTRUCTORS.items() if v["wins"] >= 10],
    })
    cats.append({
        "key": "logro:wins50", "label": "🏆🏆🏆 ≥50 victorias",
        "check": lambda t: RAW_CONSTRUCTORS[t]["wins"] >= 50,
        "teams": [t for t, v in RAW_CONSTRUCTORS.items() if v["wins"] >= 50],
    })
    cats.append({
        "key": "logro:monaco", "label": "🎰 Ganó en Mónaco",
        "check": lambda t: "monaco" in RAW_CONSTRUCTORS[t]["circuitos_victoria"],
        "teams": [t for t, v in RAW_CONSTRUCTORS.items() if "monaco" in v["circuitos_victoria"]],
    })
    cats.append({
        "key": "logro:monza", "label": "🇮🇹 Ganó en Monza",
        "check": lambda t: "monza" in RAW_CONSTRUCTORS[t]["circuitos_victoria"],
        "teams": [t for t, v in RAW_CONSTRUCTORS.items() if "monza" in v["circuitos_victoria"]],
    })
    cats.append({
        "key": "logro:silverstone", "label": "🇬🇧 Ganó en Silverstone",
        "check": lambda t: "silverstone" in RAW_CONSTRUCTORS[t]["circuitos_victoria"],
        "teams": [t for t, v in RAW_CONSTRUCTORS.items() if "silverstone" in v["circuitos_victoria"]],
    })
    cats.append({
        "key": "logro:spa", "label": "🇧🇪 Ganó en Spa",
        "check": lambda t: "spa" in RAW_CONSTRUCTORS[t]["circuitos_victoria"],
        "teams": [t for t, v in RAW_CONSTRUCTORS.items() if "spa" in v["circuitos_victoria"]],
    })
    cats.append({
        "key": "logro:suzuka", "label": "🇯🇵 Ganó en Suzuka",
        "check": lambda t: "suzuka" in RAW_CONSTRUCTORS[t]["circuitos_victoria"],
        "teams": [t for t, v in RAW_CONSTRUCTORS.items() if "suzuka" in v["circuitos_victoria"]],
    })
    cats.append({
        "key": "logro:campeon_piloto", "label": "🌟 Tuvo piloto campeón",
        "check": lambda t: len(RAW_CONSTRUCTORS[t]["pilotos_campeon"]) >= 1,
        "teams": [t for t, v in RAW_CONSTRUCTORS.items() if len(v["pilotos_campeon"]) >= 1],
    })
    cats.append({
        "key": "logro:nocampeon", "label": "❌ Nunca ganó campeonato",
        "check": lambda t: RAW_CONSTRUCTORS[t]["titles"] == 0,
        "teams": [t for t, v in RAW_CONSTRUCTORS.items() if v["titles"] == 0],
    })
    cats.append({
        "key": "logro:novictoria", "label": "❌ Nunca ganó una carrera",
        "check": lambda t: RAW_CONSTRUCTORS[t]["wins"] == 0,
        "teams": [t for t, v in RAW_CONSTRUCTORS.items() if v["wins"] == 0],
    })

    # 5. Circuitos adicionales
    CIRC_EXTRA = [
        ("interlagos",   "🇧🇷 Ganó en Interlagos"),
        ("barcelona",    "🇪🇸 Ganó en Barcelona"),
        ("nurburgring",  "🇩🇪 Ganó en Nürburgring"),
        ("hungaroring",  "🇭🇺 Ganó en Hungaroring"),
        ("melbourne",    "🇦🇺 Ganó en Melbourne"),
        ("abu dhabi",    "🇦🇪 Ganó en Abu Dhabi"),
        ("montreal",     "🇨🇦 Ganó en Montreal"),
        ("zandvoort",    "🇳🇱 Ganó en Zandvoort"),
    ]
    for circ, lbl in CIRC_EXTRA:
        teams = [t for t, v in RAW_CONSTRUCTORS.items() if circ in v["circuitos_victoria"]]
        if len(teams) >= 2:
            cats.append({
                "key":   f"logro:{circ}",
                "label": lbl,
                "check": lambda t, _c=circ: _c in RAW_CONSTRUCTORS[t]["circuitos_victoria"],
                "teams": teams,
            })

    # 6. Pilotos campeones múltiples
    cats.append({
        "key": "logro:2campeon_pilotos", "label": "🌟🌟 ≥2 pilotos campeones",
        "check": lambda t: len(RAW_CONSTRUCTORS[t]["pilotos_campeon"]) >= 2,
        "teams": [t for t, v in RAW_CONSTRUCTORS.items() if len(v["pilotos_campeon"]) >= 2],
    })

    # 7. Nunca ganó pero corrió ≥5 temporadas
    cats.append({
        "key": "logro:never_won_veteran", "label": "🏁 Sin victorias con historia",
        "check": lambda t: RAW_CONSTRUCTORS[t]["wins"] == 0 and sum(1 for d in RAW_CONSTRUCTORS[t]["epocas"]) >= 2,
        "teams": [t for t, v in RAW_CONSTRUCTORS.items()
                  if v["wins"] == 0 and len(v["epocas"]) >= 2],
    })

    # 8. Usó motor propio (nombre del equipo == motor)
    MOTORES_PROPIOS = ["ferrari", "honda", "renault", "alfa romeo", "mercedes", "maserati", "bmw"]
    cats.append({
        "key": "logro:motor_propio", "label": "⚙️ Usó motor propio",
        "check": lambda t: any(m == t.split()[0] for m in RAW_CONSTRUCTORS[t]["motores"]),
        "teams": [t for t, v in RAW_CONSTRUCTORS.items()
                  if any(m == t.split()[0] for m in v["motores"])],
    })

    # 9. Equipo que ganó su primera temporada
    cats.append({
        "key": "logro:one_season_win", "label": "⚡ Ganó en su primera época",
        "check": lambda t: (RAW_CONSTRUCTORS[t]["wins"] >= 1
                            and len(RAW_CONSTRUCTORS[t]["epocas"]) == 1),
        "teams": [t for t, v in RAW_CONSTRUCTORS.items()
                  if v["wins"] >= 1 and len(v["epocas"]) == 1],
    })

    return cats

CONSTRUCTOR_CATS = _build_constructor_categories()
ALL_CONSTRUCTORS = sorted(RAW_CONSTRUCTORS.keys())


# ══════════════════════════════════════════════════════════════════
#  MODO 2 — PODIUM CHALLENGE: Adivina el top 10
# ══════════════════════════════════════════════════════════════════

RAW_CONSTRUCTORS = {
    "ferrari": {
        "nac": "italiana", "epocas": [1950,1960,1970,1980,1990,2000,2010,2020],
        "motores": ["ferrari"],
        "titles": 16, "wins": 243,
        "circuitos_victoria": ["monaco","monza","silverstone","spa","suzuka","barcelona","bahrain","abu dhabi","budapest","melbourne","shanghai","interlagos","mexico","baku","singapore","zandvoort","imola","portimao","jeddah","montreal","hockenheim","nurburgring","austria","istanbul","valencia"],
        "pilotos_campeon": ["juan manuel fangio","mike hawthorn","phil hill","john surtees","niki lauda","jody scheckter","michael schumacher","kimi raikkonen"],
    },
    "mercedes": {
        "nac": "alemana", "epocas": [1950,2010,2020],
        "motores": ["mercedes"],
        "titles": 8, "wins": 125,
        "circuitos_victoria": ["monaco","silverstone","spa","suzuka","barcelona","bahrain","abu dhabi","budapest","melbourne","shanghai","interlagos","mexico","baku","singapore","zandvoort","imola","portimao","jeddah","montreal","austria","istanbul","nurburgring","sochi","mugello","istanbul","eifel","70th anniversary","styria","sakhir","bahrain","las vegas","qatar"],
        "pilotos_campeon": ["lewis hamilton","nico rosberg"],
    },
    "red bull": {
        "nac": "austriaca", "epocas": [2000,2010,2020],
        "motores": ["renault","honda","rbpt"],
        "titles": 7, "wins": 120,
        "circuitos_victoria": ["monaco","monza","silverstone","spa","suzuka","barcelona","bahrain","abu dhabi","budapest","melbourne","shanghai","interlagos","mexico","baku","singapore","zandvoort","imola","portimao","jeddah","montreal","austria","istanbul","nurburgring","malaysia","china","japan","qatar","las vegas"],
        "pilotos_campeon": ["sebastian vettel","max verstappen"],
    },
    "mclaren": {
        "nac": "británica", "epocas": [1960,1970,1980,1990,2000,2010,2020],
        "motores": ["ford","cosworth","chevrolet","ford","tag","honda","ford","mercedes","renault","mercedes","mercedes"],
        "titles": 8, "wins": 183,
        "circuitos_victoria": ["monaco","monza","silverstone","spa","suzuka","barcelona","bahrain","abu dhabi","budapest","melbourne","shanghai","interlagos","mexico","baku","singapore","canada","austria","malaysia","japan","san marino","imola","portimao","jeddah","las vegas","miami","zandvoort","qatar","sao paulo","saudi arabia","australia"],
        "pilotos_campeon": ["emerson fittipaldi","james hunt","niki lauda","alain prost","ayrton senna","mika hakkinen","lewis hamilton"],
    },
    "williams": {
        "nac": "británica", "epocas": [1970,1980,1990,2000,2010,2020],
        "motores": ["ford","cosworth","ford","toyota","renault","bmw","toyota","renault","mercedes","mercedes"],
        "titles": 9, "wins": 114,
        "circuitos_victoria": ["monaco","monza","silverstone","spa","suzuka","barcelona","bahrain","abu dhabi","budapest","melbourne","interlagos","canada","austria","japan","san marino","imola","nurburgring","hockenheim","portugal","france","brazil"],
        "pilotos_campeon": ["alan jones","keke rosberg","nelson piquet","nigel mansell","alain prost","damon hill","jacques villeneuve"],
    },
    "renault": {
        "nac": "francesa", "epocas": [1970,1980,2000,2010,2020],
        "motores": ["renault"],
        "titles": 2, "wins": 35,
        "circuitos_victoria": ["monaco","spa","suzuka","barcelona","bahrain","budapest","malaysia","japan","san marino","imola","nurburgring","hockenheim","austria","france","australia","canada","malaysia","bahrain","china","turkey","singapore","australia"],
        "pilotos_campeon": ["fernando alonso"],
    },
    "alpine": {
        "nac": "francesa", "epocas": [2020],
        "motores": ["renault"],
        "titles": 0, "wins": 1,
        "circuitos_victoria": ["hungary"],
        "pilotos_campeon": [],
    },
    "lotus": {
        "nac": "británica", "epocas": [1950,1960,1970,1980],
        "motores": ["climax","ford","cosworth","renault"],
        "titles": 7, "wins": 79,
        "circuitos_victoria": ["monaco","monza","silverstone","spa","suzuka","france","germany","netherlands","south africa","canada","austria","argentina","brazil","usa","portugal"],
        "pilotos_campeon": ["jim clark","jochen rindt","emerson fittipaldi","mario andretti"],
    },
    "brabham": {
        "nac": "británica", "epocas": [1960,1970,1980],
        "motores": ["climax","repco","ford","alfa romeo","cosworth","bmw"],
        "titles": 4, "wins": 35,
        "circuitos_victoria": ["monaco","monza","silverstone","spa","france","germany","netherlands","south africa","canada","austria","argentina"],
        "pilotos_campeon": ["jack brabham","denny hulme","nelson piquet"],
    },
    "tyrrell": {
        "nac": "británica", "epocas": [1960,1970,1980,1990],
        "motores": ["ford","cosworth","renault","yamaha"],
        "titles": 3, "wins": 23,
        "circuitos_victoria": ["monaco","monza","silverstone","spa","france","germany","netherlands","south africa","canada","austria","argentina","usa"],
        "pilotos_campeon": ["jackie stewart"],
    },
    "benetton": {
        "nac": "británica", "epocas": [1980,1990,2000],
        "motores": ["bmw","ford","cosworth","renault","playlife"],
        "titles": 2, "wins": 27,
        "circuitos_victoria": ["monaco","monza","silverstone","spa","suzuka","barcelona","hungary","japan","portugal","australia","canada","belgium","france","germany","san marino"],
        "pilotos_campeon": ["michael schumacher"],
    },
    "alfa romeo": {
        "nac": "italiana", "epocas": [1950,2010,2020],
        "motores": ["alfa romeo","ferrari"],
        "titles": 2, "wins": 11,
        "circuitos_victoria": ["monaco","monza","silverstone","spa","france","germany","switzerland","belgium"],
        "pilotos_campeon": ["giuseppe farina","juan manuel fangio"],
    },
    "cooper": {
        "nac": "británica", "epocas": [1950,1960],
        "motores": ["climax","maserati"],
        "titles": 2, "wins": 16,
        "circuitos_victoria": ["monaco","monza","silverstone","spa","france","germany","netherlands","south africa","usa","argentina"],
        "pilotos_campeon": ["jack brabham","bruce mclaren"],
    },
    "brm": {
        "nac": "británica", "epocas": [1950,1960,1970],
        "motores": ["brm"],
        "titles": 1, "wins": 17,
        "circuitos_victoria": ["monaco","monza","silverstone","spa","france","germany","netherlands","south africa","usa"],
        "pilotos_campeon": ["graham hill"],
    },
    "matra": {
        "nac": "francesa", "epocas": [1960,1970],
        "motores": ["ford","cosworth","matra"],
        "titles": 1, "wins": 9,
        "circuitos_victoria": ["monaco","monza","silverstone","spa","france","germany","netherlands","south africa","usa","canada"],
        "pilotos_campeon": ["jackie stewart"],
    },
    "march": {
        "nac": "británica", "epocas": [1970,1980],
        "motores": ["ford","cosworth","alfa romeo"],
        "titles": 0, "wins": 3,
        "circuitos_victoria": ["silvertone","france","sweden"],
        "pilotos_campeon": [],
    },
    "hesketh": {
        "nac": "británica", "epocas": [1970],
        "motores": ["ford","cosworth"],
        "titles": 0, "wins": 1,
        "circuitos_victoria": ["netherlands"],
        "pilotos_campeon": [],
    },
    "wolf": {
        "nac": "canadiense", "epocas": [1970],
        "motores": ["ford","cosworth"],
        "titles": 0, "wins": 3,
        "circuitos_victoria": ["argentina","monaco","canada"],
        "pilotos_campeon": [],
    },
    "shadow": {
        "nac": "estadounidense", "epocas": [1970],
        "motores": ["ford","cosworth"],
        "titles": 0, "wins": 1,
        "circuitos_victoria": ["austria"],
        "pilotos_campeon": [],
    },
    "ligier": {
        "nac": "francesa", "epocas": [1970,1980,1990],
        "motores": ["matra","ford","cosworth","renault","lamborghini","mugen"],
        "titles": 0, "wins": 9,
        "circuitos_victoria": ["sweden","argentina","brazil","spain","long beach","monaco","austria","canada","netherlands"],
        "pilotos_campeon": [],
    },
    "arrows": {
        "nac": "británica", "epocas": [1970,1980,1990,2000],
        "motores": ["ford","cosworth","bmw","megatron","ford","hart","yamaha","arrows","supertec","asiatech"],
        "titles": 0, "wins": 0,
        "circuitos_victoria": [],
        "pilotos_campeon": [],
    },
    "minardi": {
        "nac": "italiana", "epocas": [1980,1990,2000],
        "motores": ["ford","motori moderni","lamborghini","ferrari","ford","cosworth","asiatech"],
        "titles": 0, "wins": 0,
        "circuitos_victoria": [],
        "pilotos_campeon": [],
    },
    "jordan": {
        "nac": "irlandesa", "epocas": [1990,2000],
        "motores": ["ford","cosworth","yamaha","peugeot","mugen","honda","ford","bridgestone"],
        "titles": 0, "wins": 4,
        "circuitos_victoria": ["spa","monza","nurburgring","brazil","hungary"],
        "pilotos_campeon": [],
    },
    "sauber": {
        "nac": "suiza", "epocas": [1990,2000,2010,2020],
        "motores": ["ilmor","mercedes","petronas","ferrari","bmw","ferrari","honda","ferrari"],
        "titles": 0, "wins": 1,
        "circuitos_victoria": ["canada"],
        "pilotos_campeon": [],
    },
    "bar": {
        "nac": "británica", "epocas": [1990,2000],
        "motores": ["supertec","honda"],
        "titles": 0, "wins": 0,
        "circuitos_victoria": [],
        "pilotos_campeon": [],
    },
    "honda": {
        "nac": "japonesa", "epocas": [1960,2000],
        "motores": ["honda"],
        "titles": 0, "wins": 3,
        "circuitos_victoria": ["mexico","italy","hungary"],
        "pilotos_campeon": [],
    },
    "brawn gp": {
        "nac": "británica", "epocas": [2000],
        "motores": ["mercedes"],
        "titles": 1, "wins": 8,
        "circuitos_victoria": ["bahrain","australia","monaco","turkey","silverstone","valencia","brazil","japan"],
        "pilotos_campeon": ["jenson button"],
    },
    "force india": {
        "nac": "india", "epocas": [2000,2010],
        "motores": ["ferrari","mercedes"],
        "titles": 0, "wins": 3,
        "circuitos_victoria": ["spa","bahrain","monza"],
        "pilotos_campeon": [],
    },
    "racing point": {
        "nac": "británica", "epocas": [2010,2020],
        "motores": ["mercedes"],
        "titles": 0, "wins": 1,
        "circuitos_victoria": ["sakhir"],
        "pilotos_campeon": [],
    },
    "aston martin": {
        "nac": "británica", "epocas": [2020],
        "motores": ["mercedes"],
        "titles": 0, "wins": 0,
        "circuitos_victoria": [],
        "pilotos_campeon": [],
    },
    "haas": {
        "nac": "estadounidense", "epocas": [2010,2020],
        "motores": ["ferrari"],
        "titles": 0, "wins": 0,
        "circuitos_victoria": [],
        "pilotos_campeon": [],
    },
    "toro rosso": {
        "nac": "italiana", "epocas": [2000,2010],
        "motores": ["cosworth","ferrari","renault","honda"],
        "titles": 0, "wins": 1,
        "circuitos_victoria": ["monza"],
        "pilotos_campeon": [],
    },
    "alphatauri": {
        "nac": "italiana", "epocas": [2010,2020],
        "motores": ["honda","renault"],
        "titles": 0, "wins": 2,
        "circuitos_victoria": ["monza","bahrain"],
        "pilotos_campeon": [],
    },
    "rb": {
        "nac": "italiana", "epocas": [2020],
        "motores": ["honda"],
        "titles": 0, "wins": 0,
        "circuitos_victoria": [],
        "pilotos_campeon": [],
    },
    "toyota": {
        "nac": "japonesa", "epocas": [2000,2010],
        "motores": ["toyota"],
        "titles": 0, "wins": 0,
        "circuitos_victoria": [],
        "pilotos_campeon": [],
    },
    "bmw sauber": {
        "nac": "alemana", "epocas": [2000],
        "motores": ["bmw"],
        "titles": 0, "wins": 1,
        "circuitos_victoria": ["canada"],
        "pilotos_campeon": [],
    },
    "super aguri": {
        "nac": "japonesa", "epocas": [2000],
        "motores": ["honda"],
        "titles": 0, "wins": 0,
        "circuitos_victoria": [],
        "pilotos_campeon": [],
    },
    "virgin": {
        "nac": "británica", "epocas": [2010],
        "motores": ["cosworth"],
        "titles": 0, "wins": 0,
        "circuitos_victoria": [],
        "pilotos_campeon": [],
    },
    "hrt": {
        "nac": "española", "epocas": [2010],
        "motores": ["cosworth"],
        "titles": 0, "wins": 0,
        "circuitos_victoria": [],
        "pilotos_campeon": [],
    },
    "caterham": {
        "nac": "británica", "epocas": [2010],
        "motores": ["renault"],
        "titles": 0, "wins": 0,
        "circuitos_victoria": [],
        "pilotos_campeon": [],
    },
    "marussia": {
        "nac": "británica", "epocas": [2010],
        "motores": ["cosworth","ferrari"],
        "titles": 0, "wins": 0,
        "circuitos_victoria": [],
        "pilotos_campeon": [],
    },
    "maserati": {
        "nac": "italiana", "epocas": [1950],
        "motores": ["maserati"],
        "titles": 1, "wins": 9,
        "circuitos_victoria": ["argentina","belgium","france","germany","monaco","italy","pescara","morocco"],
        "pilotos_campeon": ["juan manuel fangio"],
    },
    "vanwall": {
        "nac": "británica", "epocas": [1950],
        "motores": ["vanwall"],
        "titles": 1, "wins": 9,
        "circuitos_victoria": ["silverstone","aintree","pescara","monza","spa","nurburgring","casablanca","morocco","france"],
        "pilotos_campeon": [],
    },
    "lancia": {
        "nac": "italiana", "epocas": [1950],
        "motores": ["lancia"],
        "titles": 0, "wins": 0,
        "circuitos_victoria": [],
        "pilotos_campeon": [],
    },
    "benetton ford": {
        "nac": "británica", "epocas": [1990],
        "motores": ["ford"],
        "titles": 0, "wins": 0,
        "circuitos_victoria": [],
        "pilotos_campeon": [],
    },
    "stewart": {
        "nac": "británica", "epocas": [1990],
        "motores": ["ford"],
        "titles": 0, "wins": 1,
        "circuitos_victoria": ["monaco"],
        "pilotos_campeon": [],
    },
    "prost": {
        "nac": "francesa", "epocas": [1990,2000],
        "motores": ["mugen","peugeot","ferrari"],
        "titles": 0, "wins": 0,
        "circuitos_victoria": [],
        "pilotos_campeon": [],
    },
    "techeetah": {
        "nac": "francesa", "epocas": [2010,2020],
        "motores": ["renault"],
        "titles": 0, "wins": 0,
        "circuitos_victoria": [],
        "pilotos_campeon": [],
    },
    "williams bmw": {
        "nac": "británica", "epocas": [2000],
        "motores": ["bmw"],
        "titles": 0, "wins": 0,
        "circuitos_victoria": [],
        "pilotos_campeon": [],
    },
    "kick sauber": {
        "nac": "suiza", "epocas": [2020],
        "motores": ["ferrari"],
        "titles": 0, "wins": 0,
        "circuitos_victoria": [],
        "pilotos_campeon": [],
    },
    # ── Equipos históricos adicionales ───────────────────────────
    "eagle": {
        "nac": "estadounidense", "epocas": [1960],
        "motores": ["climax","weslake"],
        "titles": 0, "wins": 1,
        "circuitos_victoria": ["spa"],
        "pilotos_campeon": [],
    },
    "honda ra272": {
        "nac": "japonesa", "epocas": [1960],
        "motores": ["honda"],
        "titles": 0, "wins": 1,
        "circuitos_victoria": ["mexico"],
        "pilotos_campeon": [],
    },
    "parnelli": {
        "nac": "estadounidense", "epocas": [1970],
        "motores": ["ford","cosworth"],
        "titles": 0, "wins": 0,
        "circuitos_victoria": [],
        "pilotos_campeon": [],
    },
    "ensign": {
        "nac": "británica", "epocas": [1970,1980],
        "motores": ["ford","cosworth"],
        "titles": 0, "wins": 0,
        "circuitos_victoria": [],
        "pilotos_campeon": [],
    },
    "fittipaldi": {
        "nac": "brasileña", "epocas": [1970,1980],
        "motores": ["ford","cosworth"],
        "titles": 0, "wins": 0,
        "circuitos_victoria": [],
        "pilotos_campeon": [],
    },
    "osella": {
        "nac": "italiana", "epocas": [1980],
        "motores": ["ford","cosworth","alfa romeo"],
        "titles": 0, "wins": 0,
        "circuitos_victoria": [],
        "pilotos_campeon": [],
    },
    "ats": {
        "nac": "alemana", "epocas": [1970,1980],
        "motores": ["ford","cosworth","bmw"],
        "titles": 0, "wins": 0,
        "circuitos_victoria": [],
        "pilotos_campeon": [],
    },
    "lola": {
        "nac": "británica", "epocas": [1960,1970,1980,1990],
        "motores": ["climax","ford","cosworth","lamborghini","ferrari","ford"],
        "titles": 0, "wins": 0,
        "circuitos_victoria": [],
        "pilotos_campeon": [],
    },
    "pacific": {
        "nac": "británica", "epocas": [1990],
        "motores": ["ford","cosworth","ilmor"],
        "titles": 0, "wins": 0,
        "circuitos_victoria": [],
        "pilotos_campeon": [],
    },
    "simtek": {
        "nac": "británica", "epocas": [1990],
        "motores": ["ford","cosworth"],
        "titles": 0, "wins": 0,
        "circuitos_victoria": [],
        "pilotos_campeon": [],
    },
    "footwork": {
        "nac": "británica", "epocas": [1990],
        "motores": ["ford","cosworth","hart","yamaha"],
        "titles": 0, "wins": 0,
        "circuitos_victoria": [],
        "pilotos_campeon": [],
    },
    "dallara": {
        "nac": "italiana", "epocas": [1990],
        "motores": ["ford","cosworth"],
        "titles": 0, "wins": 0,
        "circuitos_victoria": [],
        "pilotos_campeon": [],
    },
    "spyker": {
        "nac": "neerlandesa", "epocas": [2000],
        "motores": ["ferrari","honda"],
        "titles": 0, "wins": 0,
        "circuitos_victoria": [],
        "pilotos_campeon": [],
    },
    "midland": {
        "nac": "británica", "epocas": [2000],
        "motores": ["toyota"],
        "titles": 0, "wins": 0,
        "circuitos_victoria": [],
        "pilotos_campeon": [],
    },
    "aguri": {
        "nac": "japonesa", "epocas": [2000],
        "motores": ["honda"],
        "titles": 0, "wins": 0,
        "circuitos_victoria": [],
        "pilotos_campeon": [],
    },
    "manor": {
        "nac": "británica", "epocas": [2010],
        "motores": ["ferrari","mercedes"],
        "titles": 0, "wins": 0,
        "circuitos_victoria": [],
        "pilotos_campeon": [],
    },
}

def _build_constructor_categories():
    """Genera todas las categorías jugables para el Constructor Challenge."""
    cats = []

    NAC_FLAGS = {
        "italiana":"🇮🇹","alemana":"🇩🇪","británica":"🇬🇧","francesa":"🇫🇷",
        "austriaca":"🇦🇹","japonesa":"🇯🇵","estadounidense":"🇺🇸","suiza":"🇨🇭",
        "india":"🇮🇳","irlandesa":"🇮🇪","canadiense":"🇨🇦","española":"🇪🇸",
        "brasileña":"🇧🇷","neerlandesa":"🇳🇱",
    }
    MOTOR_FLAGS = {
        "ferrari":"🔴","mercedes":"⭐","renault":"🟡","honda":"🔵",
        "ford":"🔧","cosworth":"🔩","bmw":"⚪","tag":"🏷️",
    }

    # 1. Nacionalidad
    nacs = set(v["nac"] for v in RAW_CONSTRUCTORS.values())
    for nac in sorted(nacs):
        flag = NAC_FLAGS.get(nac, "🏁")
        teams = [t for t, v in RAW_CONSTRUCTORS.items() if v["nac"] == nac]
        if len(teams) >= 1:
            cats.append({
                "key":   f"nac:{nac}",
                "label": f"{flag} {nac.capitalize()}",
                "check": lambda t, _n=nac: RAW_CONSTRUCTORS[t]["nac"] == _n,
                "teams": teams,
            })

    # 2. Época
    EPOCAS = {
        1950: "Años 50s", 1960: "Años 60s", 1970: "Años 70s",
        1980: "Años 80s", 1990: "Años 90s", 2000: "Años 2000s",
        2010: "Años 2010s", 2020: "Años 2020s",
    }
    for dec, lbl in EPOCAS.items():
        teams = [t for t, v in RAW_CONSTRUCTORS.items() if dec in v["epocas"]]
        if len(teams) >= 1:
            cats.append({
                "key":   f"epoca:{dec}",
                "label": f"🗓️ {lbl}",
                "check": lambda t, _d=dec: _d in RAW_CONSTRUCTORS[t]["epocas"],
                "teams": teams,
            })

    # 3. Motor
    all_motors = set(m for v in RAW_CONSTRUCTORS.values() for m in v["motores"])
    for motor in sorted(all_motors):
        teams = [t for t, v in RAW_CONSTRUCTORS.items() if motor in v["motores"]]
        if len(teams) >= 2:
            flag = MOTOR_FLAGS.get(motor, "⚙️")
            cats.append({
                "key":   f"motor:{motor}",
                "label": f"{flag} Motor {motor.capitalize()}",
                "check": lambda t, _m=motor: _m in RAW_CONSTRUCTORS[t]["motores"],
                "teams": teams,
            })

    # 4. Logros
    cats.append({
        "key": "logro:campeon", "label": "👑 Ganó Campeonato",
        "check": lambda t: RAW_CONSTRUCTORS[t]["titles"] >= 1,
        "teams": [t for t, v in RAW_CONSTRUCTORS.items() if v["titles"] >= 1],
    })
    cats.append({
        "key": "logro:5titles", "label": "👑👑 ≥5 Campeonatos",
        "check": lambda t: RAW_CONSTRUCTORS[t]["titles"] >= 5,
        "teams": [t for t, v in RAW_CONSTRUCTORS.items() if v["titles"] >= 5],
    })
    cats.append({
        "key": "logro:wins1", "label": "🏆 Al menos 1 victoria",
        "check": lambda t: RAW_CONSTRUCTORS[t]["wins"] >= 1,
        "teams": [t for t, v in RAW_CONSTRUCTORS.items() if v["wins"] >= 1],
    })
    cats.append({
        "key": "logro:wins10", "label": "🏆🏆 ≥10 victorias",
        "check": lambda t: RAW_CONSTRUCTORS[t]["wins"] >= 10,
        "teams": [t for t, v in RAW_CONSTRUCTORS.items() if v["wins"] >= 10],
    })
    cats.append({
        "key": "logro:wins50", "label": "🏆🏆🏆 ≥50 victorias",
        "check": lambda t: RAW_CONSTRUCTORS[t]["wins"] >= 50,
        "teams": [t for t, v in RAW_CONSTRUCTORS.items() if v["wins"] >= 50],
    })
    cats.append({
        "key": "logro:monaco", "label": "🎰 Ganó en Mónaco",
        "check": lambda t: "monaco" in RAW_CONSTRUCTORS[t]["circuitos_victoria"],
        "teams": [t for t, v in RAW_CONSTRUCTORS.items() if "monaco" in v["circuitos_victoria"]],
    })
    cats.append({
        "key": "logro:monza", "label": "🇮🇹 Ganó en Monza",
        "check": lambda t: "monza" in RAW_CONSTRUCTORS[t]["circuitos_victoria"],
        "teams": [t for t, v in RAW_CONSTRUCTORS.items() if "monza" in v["circuitos_victoria"]],
    })
    cats.append({
        "key": "logro:silverstone", "label": "🇬🇧 Ganó en Silverstone",
        "check": lambda t: "silverstone" in RAW_CONSTRUCTORS[t]["circuitos_victoria"],
        "teams": [t for t, v in RAW_CONSTRUCTORS.items() if "silverstone" in v["circuitos_victoria"]],
    })
    cats.append({
        "key": "logro:spa", "label": "🇧🇪 Ganó en Spa",
        "check": lambda t: "spa" in RAW_CONSTRUCTORS[t]["circuitos_victoria"],
        "teams": [t for t, v in RAW_CONSTRUCTORS.items() if "spa" in v["circuitos_victoria"]],
    })
    cats.append({
        "key": "logro:suzuka", "label": "🇯🇵 Ganó en Suzuka",
        "check": lambda t: "suzuka" in RAW_CONSTRUCTORS[t]["circuitos_victoria"],
        "teams": [t for t, v in RAW_CONSTRUCTORS.items() if "suzuka" in v["circuitos_victoria"]],
    })
    cats.append({
        "key": "logro:campeon_piloto", "label": "🌟 Tuvo piloto campeón",
        "check": lambda t: len(RAW_CONSTRUCTORS[t]["pilotos_campeon"]) >= 1,
        "teams": [t for t, v in RAW_CONSTRUCTORS.items() if len(v["pilotos_campeon"]) >= 1],
    })
    cats.append({
        "key": "logro:nocampeon", "label": "❌ Nunca ganó campeonato",
        "check": lambda t: RAW_CONSTRUCTORS[t]["titles"] == 0,
        "teams": [t for t, v in RAW_CONSTRUCTORS.items() if v["titles"] == 0],
    })
    cats.append({
        "key": "logro:novictoria", "label": "❌ Nunca ganó una carrera",
        "check": lambda t: RAW_CONSTRUCTORS[t]["wins"] == 0,
        "teams": [t for t, v in RAW_CONSTRUCTORS.items() if v["wins"] == 0],
    })

    # 5. Circuitos adicionales
    CIRC_EXTRA = [
        ("interlagos",   "🇧🇷 Ganó en Interlagos"),
        ("barcelona",    "🇪🇸 Ganó en Barcelona"),
        ("nurburgring",  "🇩🇪 Ganó en Nürburgring"),
        ("hungaroring",  "🇭🇺 Ganó en Hungaroring"),
        ("melbourne",    "🇦🇺 Ganó en Melbourne"),
        ("abu dhabi",    "🇦🇪 Ganó en Abu Dhabi"),
        ("montreal",     "🇨🇦 Ganó en Montreal"),
        ("zandvoort",    "🇳🇱 Ganó en Zandvoort"),
    ]
    for circ, lbl in CIRC_EXTRA:
        teams = [t for t, v in RAW_CONSTRUCTORS.items() if circ in v["circuitos_victoria"]]
        if len(teams) >= 2:
            cats.append({
                "key":   f"logro:{circ}",
                "label": lbl,
                "check": lambda t, _c=circ: _c in RAW_CONSTRUCTORS[t]["circuitos_victoria"],
                "teams": teams,
            })

    # 6. Pilotos campeones múltiples
    cats.append({
        "key": "logro:2campeon_pilotos", "label": "🌟🌟 ≥2 pilotos campeones",
        "check": lambda t: len(RAW_CONSTRUCTORS[t]["pilotos_campeon"]) >= 2,
        "teams": [t for t, v in RAW_CONSTRUCTORS.items() if len(v["pilotos_campeon"]) >= 2],
    })

    # 7. Nunca ganó pero corrió ≥5 temporadas
    cats.append({
        "key": "logro:never_won_veteran", "label": "🏁 Sin victorias con historia",
        "check": lambda t: RAW_CONSTRUCTORS[t]["wins"] == 0 and sum(1 for d in RAW_CONSTRUCTORS[t]["epocas"]) >= 2,
        "teams": [t for t, v in RAW_CONSTRUCTORS.items()
                  if v["wins"] == 0 and len(v["epocas"]) >= 2],
    })

    # 8. Usó motor propio (nombre del equipo == motor)
    MOTORES_PROPIOS = ["ferrari", "honda", "renault", "alfa romeo", "mercedes", "maserati", "bmw"]
    cats.append({
        "key": "logro:motor_propio", "label": "⚙️ Usó motor propio",
        "check": lambda t: any(m == t.split()[0] for m in RAW_CONSTRUCTORS[t]["motores"]),
        "teams": [t for t, v in RAW_CONSTRUCTORS.items()
                  if any(m == t.split()[0] for m in v["motores"])],
    })

    # 9. Equipo que ganó su primera temporada
    cats.append({
        "key": "logro:one_season_win", "label": "⚡ Ganó en su primera época",
        "check": lambda t: (RAW_CONSTRUCTORS[t]["wins"] >= 1
                            and len(RAW_CONSTRUCTORS[t]["epocas"]) == 1),
        "teams": [t for t, v in RAW_CONSTRUCTORS.items()
                  if v["wins"] >= 1 and len(v["epocas"]) == 1],
    })

    return cats

CONSTRUCTOR_CATS = _build_constructor_categories()
ALL_CONSTRUCTORS = sorted(RAW_CONSTRUCTORS.keys())


# ══════════════════════════════════════════════════════════════════
#  MODO 2 — PODIUM CHALLENGE: Adivina el top 10
# ══════════════════════════════════════════════════════════════════
class PodiumGame:
    def __init__(self):
        self._build_ui()

    def _build_ui(self):
        import datetime

        self.output = widgets.Output()

        title = widgets.HTML(
            "<h2 style='font-family:monospace;margin:0;color:#e10600'>"
            "🏆 PODIUM CHALLENGE</h2>"
            "<p style='font-family:monospace;font-size:12px;color:gray;margin:2px 0'>"
            "Adivina el Top 10 de un Gran Premio · Solo el año y la carrera como pista</p>"
        )

        # ── Selector de año ──
        years = sorted(GP_RESULTS.keys(), reverse=True)
        self.year_sel = widgets.Dropdown(
            options=years, value=years[0], description="Año:",
            style={"description_width": "40px"},
            layout=widgets.Layout(width="110px"),
        )
        self.year_sel.observe(self._on_year_change, names="value")

        # ── Selector de GP ──
        self.gp_sel = widgets.Dropdown(
            options=list(GP_RESULTS[years[0]].keys()),
            description="GP:",
            style={"description_width": "30px"},
            layout=widgets.Layout(width="310px"),
        )

        # ── Filtros para modo aleatorio ──
        all_years = sorted(GP_RESULTS.keys())
        era_opts = [
            ("Todas las épocas", (min(all_years), max(all_years))),
            ("Clásicos (≤1999)",  (min(all_years), 1999)),
            ("2000s",             (2000, 2009)),
            ("2010s",             (2010, 2019)),
            ("Recientes (2020+)", (2020, max(all_years))),
        ]
        self.era_sel = widgets.Dropdown(
            options=[(lbl, rng) for lbl, rng in era_opts],
            value=era_opts[0][1],
            description="Época:",
            style={"description_width": "55px"},
            layout=widgets.Layout(width="220px"),
        )

        # Circuitos únicos para filtrar
        all_circuits = sorted(set(
            gp for gps in GP_RESULTS.values() for gp in gps
        ))
        self.circuit_sel = widgets.Dropdown(
            options=[("Cualquier circuito", None)] + [(c, c) for c in all_circuits],
            value=None,
            description="Circuito:",
            style={"description_width": "62px"},
            layout=widgets.Layout(width="310px"),
        )

        # ── Botones ──
        self.btn_new    = widgets.Button(description="▶ Elegir Carrera", button_style="success",
                                         layout=widgets.Layout(width="155px"))
        self.btn_random = widgets.Button(description="🎲 Aleatoria",     button_style="warning",
                                         layout=widgets.Layout(width="130px"))
        self.btn_check  = widgets.Button(description="✔ Verificar",     button_style="primary",
                                         layout=widgets.Layout(width="120px"), disabled=True)
        self.btn_reveal = widgets.Button(description="💡 Revelar",       button_style="info",
                                         layout=widgets.Layout(width="110px"), disabled=True)
        self.btn_daily  = widgets.ToggleButton(value=False, description="📅 Diario",
                                               button_style="", layout=widgets.Layout(width="100px"))

        self.score_label = widgets.HTML(
            "<span style='font-family:monospace;font-size:14px'>─</span>"
        )
        self.pts_label = widgets.HTML(
            "<span style='font-family:monospace;font-size:13px'>⭐ 0 pts</span>"
        )
        self._refresh_pts()

        self.btn_new.on_click(self._start_race)
        self.btn_random.on_click(self._start_random)
        self.btn_check.on_click(self._check)
        self.btn_reveal.on_click(self._reveal)
        self.btn_daily.observe(self._on_daily_toggle, names="value")

        self.grid_out = widgets.Output()

        controls = widgets.HBox(
            [self.year_sel, self.gp_sel],
            layout=widgets.Layout(gap="8px", align_items="center"),
        )
        random_bar = widgets.HBox(
            [widgets.HTML("<span style='font-family:monospace;font-size:12px;"
                          "color:#f9a825;font-weight:bold'>🎲 Modo Aleatorio →</span>"),
             self.era_sel, self.circuit_sel],
            layout=widgets.Layout(gap="8px", align_items="center",
                                  flex_flow="row wrap", margin="4px 0"),
        )
        action_bar = widgets.HBox(
            [self.btn_new, self.btn_random, self.btn_check, self.btn_reveal,
             self.btn_daily, self.score_label, self.pts_label],
            layout=widgets.Layout(gap="8px", align_items="center",
                                  flex_flow="row wrap", margin="8px 0"),
        )

        self.main_widget = widgets.VBox(
            [title, controls, random_bar, action_bar, self.grid_out, self.output],
            layout=widgets.Layout(padding="14px", border="2px solid #1565c0",
                                   border_radius="10px", max_width="720px"),
        )
        display(self.main_widget)

    # ── Helpers ──────────────────────────────────────────────────
    def _data_path(self):
        import os
        return os.path.expanduser("~/.f1grid_data.json")

    def _load_data(self):
        import json, os
        try:
            p = self._data_path()
            if os.path.exists(p):
                with open(p) as f:
                    return json.load(f)
        except Exception:
            pass
        return {"streak": {"current":0,"best":0,"last_date":""},
                "history": [], "daily_played": {}, "total_pts": 0}

    def _save_data(self, data):
        import json
        try:
            with open(self._data_path(), "w") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception:
            pass

    def _refresh_pts(self):
        data = self._load_data()
        pts  = data.get("total_pts", 0)
        self.pts_label.value = (
            f"<span style='font-family:monospace;font-size:13px'>⭐ {pts} pts</span>"
        )

    def _on_year_change(self, change):
        year = change["new"]
        self.gp_sel.options = list(GP_RESULTS.get(year, {}).keys())

    def _on_daily_toggle(self, change):
        self.btn_daily.description = "📅 Diario ON" if change["new"] else "📅 Diario"
        self.btn_daily.button_style = "warning" if change["new"] else ""

    def _daily_seed(self):
        import hashlib, datetime
        today  = datetime.date.today().isoformat()
        key    = f"podium-{today}"
        digest = int(hashlib.md5(key.encode()).hexdigest(), 16)
        return digest % (2**31)

    def _already_played_today(self):
        import datetime
        today = datetime.date.today().isoformat()
        key   = f"podium-daily-{today}"
        return self._load_data().get("daily_played", {}).get(key, False)

    def _mark_daily_played(self):
        import datetime
        today = datetime.date.today().isoformat()
        key   = f"podium-daily-{today}"
        data  = self._load_data()
        data.setdefault("daily_played", {})[key] = True
        self._save_data(data)

    def _add_pts(self, pts):
        data = self._load_data()
        data["total_pts"] = data.get("total_pts", 0) + pts
        self._save_data(data)
        self._refresh_pts()

    # ── Iniciar carrera ──────────────────────────────────────────
    def _start_race(self, b=None):
        import random, datetime

        if self.btn_daily.value:
            if self._already_played_today():
                with self.output:
                    clear_output()
                    print("🔒 Ya jugaste el Podium del día. ¡Vuelve mañana!")
                return
            seed  = self._daily_seed()
            rng   = random.Random(seed)
            # Pick race deterministically
            all_races = [(yr, gp) for yr, gps in GP_RESULTS.items()
                         for gp in gps if len(GP_RESULTS[yr][gp]) == 10]
            self.year, self.gp = rng.choice(all_races)
        else:
            year = self.year_sel.value
            gp   = self.gp_sel.value
            # Validate has 10 results
            if len(GP_RESULTS.get(year, {}).get(gp, [])) < 10:
                with self.output:
                    clear_output()
                    print(f"⚠️  {gp} {year} no tiene datos completos (menos de 10 pilotos).")
                return
            self.year, self.gp = year, gp

        self.answer = [normalize(d) for d in GP_RESULTS[self.year][self.gp]]
        self._build_inputs()
        self.btn_check.disabled  = False
        self.btn_reveal.disabled = False
        self.score_label.value   = "<span style='font-family:monospace'>─</span>"
        with self.output:
            clear_output()

    # ── Modo Aleatorio ───────────────────────────────────────────
    def _start_random(self, b=None):
        import random

        era_range   = self.era_sel.value          # (year_min, year_max) o None
        circuit_flt = self.circuit_sel.value      # str o None

        # Construir pool filtrado
        pool = [
            (yr, gp)
            for yr, gps in GP_RESULTS.items()
            for gp in gps
            if len(GP_RESULTS[yr][gp]) == 10
            and (era_range is None or era_range[0] <= yr <= era_range[1])
            and (circuit_flt is None or gp == circuit_flt)
        ]

        if not pool:
            with self.output:
                clear_output()
                print("⚠️  No hay carreras con esos filtros. Prueba otra combinación.")
            return

        self.year, self.gp = random.choice(pool)
        # Sincronizar selectores manuales (visual)
        if self.year in [o for o in self.year_sel.options]:
            self.year_sel.value = self.year
        if self.gp in [o for o in self.gp_sel.options]:
            self.gp_sel.value = self.gp

        self.answer = [normalize(d) for d in GP_RESULTS[self.year][self.gp]]
        self._build_inputs(random_mode=True)
        self.btn_check.disabled  = False
        self.btn_reveal.disabled = False
        self.score_label.value   = "<span style='font-family:monospace'>─</span>"
        with self.output:
            clear_output()

    # ── Construir celdas ─────────────────────────────────────────
    def _build_inputs(self, random_mode=False):
        self.inputs = {}

        # Driver options for autocomplete — union of GP drivers + all F1 series drivers
        all_opts = sorted(set(
            d.title() for d in _ALL_GP_DRIVERS
        ) | set(
            d.title() for d in SERIES_MAP["🏎️ Fórmula 1"].drivers_meta
        ))

        pos_colors = ["#ffd700","#c0c0c0","#cd7f32"] + ["#1a1a2e"] * 7
        pos_labels  = ["🥇 P1","🥈 P2","🥉 P3"] + [f"   P{i}" for i in range(4,11)]

        rows = []
        for i in range(10):
            pos_html = widgets.HTML(
                f"<span style='font-family:monospace;font-weight:bold;"
                f"font-size:13px;color:{pos_colors[i]};width:52px;"
                f"display:inline-block'>{pos_labels[i]}</span>"
            )
            combo = widgets.Combobox(
                placeholder=f"Piloto en posición {i+1}...",
                options=all_opts,
                ensure_option=False,
                layout=widgets.Layout(width="280px", height="32px"),
            )

            # Live border feedback
            def _on_change(change, _i=i):
                inp    = self.inputs[_i]
                driver = normalize(change["new"])
                if not driver:
                    inp.layout.border = "1px solid #555"
                elif driver in self.answer:
                    inp.layout.border = "2px solid #2e7d32"  # green = in top10
                else:
                    inp.layout.border = "2px solid #f9a825"  # yellow = not in DB
            combo.observe(_on_change, names="value")
            self.inputs[i] = combo
            rows.append(widgets.HBox([pos_html, combo],
                                      layout=widgets.Layout(align_items="center", gap="6px")))

        # Badge de modo
        mode_badge = (
            "<span style='background:#f9a825;color:#000;font-family:monospace;"
            "font-size:11px;font-weight:bold;padding:2px 8px;border-radius:4px;"
            "margin-left:8px'>🎲 ALEATORIO</span>"
            if random_mode else ""
        )

        # Header
        header = widgets.HTML(
            f"<div style='font-family:monospace;font-size:15px;font-weight:bold;"
            f"color:#e10600;margin-bottom:8px'>"
            f"📍 {self.gp} · {self.year}{mode_badge}</div>"
            f"<div style='font-family:monospace;font-size:12px;color:gray;margin-bottom:10px'>"
            f"Escribe los 10 pilotos del Top 10 (en cualquier orden — puntos solo por posición exacta)</div>"
        )

        with self.grid_out:
            clear_output(wait=True)
            display(widgets.VBox([header] + rows,
                                  layout=widgets.Layout(gap="4px")))

    # ── Verificar ────────────────────────────────────────────────
    def _check(self, b=None):
        correct_pos   = 0   # exact position
        correct_any   = 0   # in top10 but wrong position
        used_indices  = set()

        result_rows = []
        for i in range(10):
            inp    = self.inputs[i]
            driver = normalize(inp.value)

            if not driver:
                inp.layout.border = "1px solid #555"
                result_rows.append(f"   P{i+1:>2}  ⬜  (vacío)")
                continue

            if driver == self.answer[i]:
                inp.layout.border = "3px solid #2e7d32"
                correct_pos += 1
                correct_any += 1
                used_indices.add(i)
                result_rows.append(f"   P{i+1:>2}  🟩  {inp.value.title()}")
            elif driver in self.answer:
                real_pos = self.answer.index(driver) + 1
                inp.layout.border = "3px solid #f9a825"
                correct_any += 1
                result_rows.append(f"   P{i+1:>2}  🟨  {inp.value.title()}  (era P{real_pos})")
            else:
                inp.layout.border = "3px solid #e10600"
                result_rows.append(f"   P{i+1:>2}  🟥  {inp.value.title()}  (no en top 10)")

        # Score: 100 pts per exact position, 20 pts per correct-but-wrong-position
        pts = correct_pos * 100 + (correct_any - correct_pos) * 20

        self.score_label.value = (
            f"<span style='font-family:monospace;font-size:13px'>"
            f"🟩 {correct_pos}/10 exactos &nbsp; 🟨 {correct_any - correct_pos} posición errónea"
            f" &nbsp; ⭐ {pts} pts</span>"
        )

        with self.output:
            clear_output()
            print(f"{'─'*44}")
            print(f"  {self.gp} · {self.year}")
            print(f"{'─'*44}")
            for row in result_rows:
                print(row)
            print(f"{'─'*44}")
            print(f"  🟩 Posición exacta : {correct_pos}/10  (+{correct_pos*100} pts)")
            print(f"  🟨 En top 10       : {correct_any - correct_pos}    (+{(correct_any-correct_pos)*20} pts)")
            print(f"  ⭐ Total esta carrera: {pts} pts")

        if pts > 0:
            self._add_pts(pts)
            if self.btn_daily.value and correct_pos == 10:
                self._mark_daily_played()

        if correct_pos == 10:
            with self.output:
                print(f"\n🏆 ¡PERFECTO! Top 10 completo y en orden exacto")

    # ── Revelar respuesta ────────────────────────────────────────
    def _reveal(self, b=None):
        with self.output:
            clear_output()
            print(f"{'─'*40}")
            print(f"  Resultado real: {self.gp} · {self.year}")
            print(f"{'─'*40}")
            medals = ["🥇","🥈","🥉"] + ["  "] * 7
            for i, driver in enumerate(self.answer):
                print(f"  {medals[i]} P{i+1:>2}  {driver.title()}")
            print(f"{'─'*40}")
        # Fill inputs with correct answers in green
        for i, driver in enumerate(self.answer):
            self.inputs[i].value = driver.title()
            self.inputs[i].layout.border = "2px solid #555"
        self.btn_check.disabled  = True
        self.btn_reveal.disabled = True


# ══════════════════════════════════════════════════════════════════
#  LANZADOR — selector de modo de juego
# ══════════════════════════════════════════════════════════════════
#  MODO 4 — CONSTRUCTOR CHALLENGE: Adivina la escudería
# ══════════════════════════════════════════════════════════════════

F1_EVENTS = [
    # ── Debuts de pilotos ────────────────────────────────────────
    (1950, "Debut de Juan Manuel Fangio en F1",                         "debut"),
    (1958, "Debut de Stirling Moss como piloto independiente icónico",  "debut"),
    (1960, "Debut de Jim Clark en F1",                                  "debut"),
    (1968, "Debut de Jackie Stewart en F1",                             "debut"),
    (1970, "Debut de Emerson Fittipaldi en F1",                        "debut"),
    (1972, "Debut de Niki Lauda en F1",                                 "debut"),
    (1974, "Debut de James Hunt en F1",                                 "debut"),
    (1978, "Debut de Gilles Villeneuve en F1",                          "debut"),
    (1980, "Debut de Alain Prost en F1",                                "debut"),
    (1980, "Debut de Nigel Mansell en F1",                              "debut"),
    (1984, "Debut de Ayrton Senna en F1",                               "debut"),
    (1987, "Debut de Michael Schumacher en F1",                         "debut"),  # Jordan 1991, pero 1987 es su karting peak — usar 1991
    (1991, "Debut de Michael Schumacher en F1 (Jordan, Bélgica)",       "debut"),
    (1993, "Debut de David Coulthard en F1",                            "debut"),
    (1994, "Debut de Mika Häkkinen como piloto titular McLaren",        "debut"),
    (1996, "Debut de Jacques Villeneuve en F1",                         "debut"),
    (1998, "Debut de Kimi Räikkönen en Sauber",                        "debut"),  # 2001 en realidad
    (2001, "Debut de Kimi Räikkönen en F1 (Sauber)",                   "debut"),
    (2000, "Debut de Jenson Button en F1",                              "debut"),
    (2001, "Debut de Juan Pablo Montoya en F1",                         "debut"),
    (2007, "Debut de Lewis Hamilton en F1 (McLaren)",                   "debut"),
    (2007, "Debut de Nico Rosberg en F1",                               "debut"),
    (2007, "Debut de Sebastian Vettel en F1 (BMW Sauber)",              "debut"),
    (2009, "Debut de Nico Hülkenberg en F1",                            "debut"),
    (2010, "Debut de Paul di Resta en F1",                              "debut"),
    (2015, "Debut de Max Verstappen en F1 (Toro Rosso, 17 años)",       "debut"),
    (2015, "Debut de Carlos Sainz en F1",                               "debut"),
    (2015, "Debut de Lando Norris en la academia McLaren",              "debut"),
    (2018, "Debut de Lando Norris en F1",                               "debut"),  # 2019
    (2019, "Debut de Lando Norris en F1 (McLaren)",                     "debut"),
    (2019, "Debut de George Russell en F1 (Williams)",                  "debut"),
    (2019, "Debut de Alexander Albon en F1",                            "debut"),
    (2021, "Debut de Yuki Tsunoda en F1",                               "debut"),
    (2022, "Debut de Zhou Guanyu en F1",                                "debut"),
    (2023, "Debut de Oscar Piastri en F1 (McLaren)",                    "debut"),
    (2024, "Debut de Oliver Bearman en F1 (sustituyendo a Sainz en Ferrari)", "debut"),

    # ── Primeros títulos de constructores ────────────────────────
    (1950, "Alfa Romeo gana el primer Campeonato del Mundo de F1",      "titulo"),
    (1952, "Ferrari gana su primer título de constructores",            "titulo"),
    (1958, "Vanwall gana el primer Campeonato de Constructores oficial","titulo"),
    (1959, "Cooper gana su primer título de constructores",             "titulo"),
    (1963, "Lotus gana su primer título de constructores",              "titulo"),
    (1966, "Brabham gana el título — primer equipo en ganar con auto propio", "titulo"),
    (1973, "Tyrrell gana el título de constructores",                   "titulo"),
    (1974, "McLaren gana su primer título de constructores",            "titulo"),
    (1979, "Ferrari gana el título tras dominio Scheckter",             "titulo"),
    (1980, "Williams gana su primer título de constructores",           "titulo"),
    (1984, "McLaren domina con Lauda y Prost, gana constructores",      "titulo"),
    (1992, "Williams gana el título con Mansell dominando",             "titulo"),
    (1994, "Benetton gana su primer título con Schumacher",             "titulo"),
    (1998, "McLaren gana el título con Häkkinen campeón",               "titulo"),
    (1999, "Ferrari gana el título de constructores sin ganar pilotos", "titulo"),
    (2009, "Brawn GP gana el título en su única temporada en F1",       "titulo"),
    (2010, "Red Bull gana su primer título de constructores",           "titulo"),
    (2014, "Mercedes domina la era híbrida, primer título de constructores", "titulo"),
    (2022, "Red Bull gana el título con Verstappen y Pérez",            "titulo"),

    # ── Accidentes / retiros famosos ─────────────────────────────
    (1955, "Accidente de Le Mans — más de 80 muertos, Mercedes se retira de F1", "accidente"),
    (1958, "Muerte de Mike Hawthorn en accidente de tráfico tras ser campeón",   "accidente"),
    (1960, "Muerte de Chris Bristow y Alan Stacey en el GP de Bélgica",          "accidente"),
    (1968, "Muerte de Jim Clark en Hockenheim — F2",                             "accidente"),
    (1970, "Muerte de Jochen Rindt en Monza — campeón póstumo",                  "accidente"),
    (1973, "Muerte de Roger Williamson en el GP de Países Bajos",                "accidente"),
    (1975, "Accidente de Niki Lauda en Nürburgring — quemaduras graves",         "accidente"),
    (1977, "Muerte de Tom Pryce en Sudáfrica tras colisión en pit",              "accidente"),
    (1978, "Muerte de Ronnie Peterson en Monza por accidente al inicio",         "accidente"),
    (1982, "Muerte de Gilles Villeneuve en clasificación en Zolder",             "accidente"),
    (1982, "Muerte de Didier Pironi termina su carrera en Hockenheim",           "accidente"),
    (1994, "Muerte de Ayrton Senna en Imola, GP de San Marino",                 "accidente"),
    (1994, "Muerte de Roland Ratzenberger en Imola, día antes que Senna",       "accidente"),
    (1999, "Michael Schumacher se fractura la pierna en Silverstone",            "accidente"),
    (2009, "Accidente de Felipe Massa en Hungría — casi pierde la vida",         "accidente"),
    (2014, "Jules Bianchi sufre accidente grave en el GP de Japón",              "accidente"),
    (2015, "Muerte de Jules Bianchi por lesiones del accidente de Japón",        "accidente"),
    (2020, "Romain Grosjean escapa de un auto en llamas en Bahréin",             "accidente"),
    (2022, "Zhou Guanyu sobrevive accidente espectacular en Silverstone",         "accidente"),

    # ── Cambios de reglamento / hitos técnicos ───────────────────
    (1950, "Primera carrera del Campeonato Mundial de F1 en Silverstone",        "reglamento"),
    (1952, "F1 cambia temporalmente a motores F2 por falta de entradas",         "reglamento"),
    (1958, "Se introduce el Campeonato de Constructores oficialmente",            "reglamento"),
    (1961, "Se reduce la cilindrada a 1.5 litros — era de los 'teapots'",        "reglamento"),
    (1966, "Se duplica la cilindrada a 3.0 litros — comienzo de la era DFV",     "reglamento"),
    (1968, "Se permite publicidad comercial en los autos por primera vez",        "reglamento"),
    (1969, "Se introducen los alerones aerodinámicos en F1",                     "reglamento"),
    (1977, "Lotus presenta el efecto suelo — revolución aerodinámica",           "reglamento"),
    (1983, "Se prohíbe el efecto suelo en F1",                                   "reglamento"),
    (1988, "Turbo prohibido — último año de los turbos de 1.5L",                 "reglamento"),
    (1994, "Se prohíben ayudas electrónicas: tracción, suspensión activa",       "reglamento"),
    (1998, "Se introducen los neumáticos ranurados y se achica el ancho",        "reglamento"),
    (2005, "Prohibición de cambiar neumáticos durante la carrera",               "reglamento"),
    (2009, "Introducción del KERS (recuperación de energía cinética)",           "reglamento"),
    (2010, "Reintroducción de reabastecimiento eliminada — sin repostar en carrera", "reglamento"),
    (2011, "Introducción del DRS (Drag Reduction System)",                       "reglamento"),
    (2014, "Era híbrida: motores V6 turbo con MGU-H y MGU-K",                   "reglamento"),
    (2017, "Autos más anchos y más carga aerodinámica — vuelta a la velocidad", "reglamento"),
    (2021, "Introducción del formato Sprint (clasificación al sprint)",          "reglamento"),
    (2022, "Revolución técnica: efecto suelo vuelve con los autos de 'ground effect'", "reglamento"),
    (2026, "Nuevo reglamento de motores: motores 100% sostenibles anunciados",  "reglamento"),

    # ── Victorias icónicas ───────────────────────────────────────
    (1967, "Primera victoria de la historia con motor Cosworth DFV — Jim Clark en Zandvoort", "victoria"),
    (1971, "Peter Gethin gana Monza por 0.01s — la carrera más reñida de la historia",        "victoria"),
    (1981, "Gilles Villeneuve gana Mónaco en el Williams de Pironi — batalla épica",           "victoria"),
    (1984, "Ayrton Senna gana su primera carrera en F1 — GP de Portugal",                     "victoria"),
    (1985, "Alain Prost gana su primer campeonato del mundo",                                  "victoria"),
    (1989, "Senna y Prost chocan en Suzuka — Prost gana el título",                           "victoria"),
    (1992, "Nigel Mansell gana el título con un récord de 9 victorias en una temporada",       "victoria"),
    (1993, "Senna gana Donington en la lluvia — considerada la mejor vuelta de la historia",   "victoria"),
    (1996, "Damon Hill gana su único campeonato del mundo en Japón",                          "victoria"),
    (2000, "Michael Schumacher gana en Japón — su primer título con Ferrari en 21 años",      "victoria"),
    (2003, "Kimi Räikkönen pierde el título por 2 puntos ante Schumacher en la última carrera","victoria"),
    (2005, "Fernando Alonso se convierte en el campeón más joven hasta ese momento",           "victoria"),
    (2008, "Lewis Hamilton gana su primer título en la última vuelta del último GP",           "victoria"),
    (2010, "Sebastian Vettel gana el título en Abu Dhabi en la última carrera",               "victoria"),
    (2012, "Vettel remonta de último a campeón en Brasil — último GP de la temporada",        "victoria"),
    (2016, "Primera victoria de Max Verstappen en F1 — GP de España, 18 años",               "victoria"),
    (2017, "Lewis Hamilton iguala el récord de Schumacher de 91 victorias",                   "victoria"),
    (2019, "Pierre Gasly gana el GP de Italia — victoria sorpresa de AlphaTauri",             "victoria"),
    (2020, "Sergio Pérez gana el GP de Sakhir — primera victoria de Racing Point",            "victoria"),
    (2021, "Max Verstappen gana el título en la última vuelta del último GP ante Hamilton",    "victoria"),
    (2021, "Doblete de McLaren en Monza — Ricciardo y Norris 1-2",                            "victoria"),
    (2022, "Carlos Sainz gana su primera carrera en F1 — GP de Gran Bretaña",                "victoria"),
    (2023, "Max Verstappen rompe el récord de 13 victorias consecutivas en una temporada",    "victoria"),
    (2024, "Lando Norris gana su primera carrera en F1 — GP de Miami",                       "victoria"),
    (2024, "McLaren gana el título de constructores por primera vez desde 1998",              "victoria"),
    (2025, "Lando Norris se corona campeón del mundo por primera vez",                        "victoria"),

    # ── Poles y récords ──────────────────────────────────────────
    (1986, "Ayrton Senna consigue su primera pole position en F1",                            "record"),
    (1988, "McLaren gana 15 de 16 carreras — la dominancia más grande de la historia",        "record"),
    (1988, "Ayrton Senna logra 13 poles en una sola temporada",                               "record"),
    (2002, "Michael Schumacher gana el título con 6 carreras de antelación",                  "record"),
    (2004, "Michael Schumacher gana 13 carreras en una temporada — récord de la época",       "record"),
    (2013, "Sebastian Vettel gana 9 carreras consecutivas al final de temporada",             "record"),
    (2014, "Mercedes gana 16 de 19 carreras en la primera temporada híbrida",                 "record"),
    (2016, "Lewis Hamilton logra su 50ª pole position en F1",                                 "record"),
    (2020, "Lewis Hamilton supera el récord de 91 victorias de Schumacher",                   "record"),
    (2020, "Lewis Hamilton iguala los 7 títulos mundiales de Michael Schumacher",             "record"),
    (2023, "Max Verstappen logra 19 victorias en una sola temporada — récord absoluto",       "record"),
]

# Eliminar duplicados por descripción exacta
_seen = set()
F1_EVENTS_CLEAN = []
for ev in F1_EVENTS:
    if ev[1] not in _seen:
        _seen.add(ev[1])
        F1_EVENTS_CLEAN.append(ev)
F1_EVENTS = F1_EVENTS_CLEAN


# ══════════════════════════════════════════════════════════════════
#  MODO 5 — LÍNEA DE TIEMPO: Ordená los eventos
# ══════════════════════════════════════════════════════════════════

# ══════════════════════════════════════════════════════════════════
#  MODO 7 — CADENA DE PILOTOS: grafo de compañeros reales
# ══════════════════════════════════════════════════════════════════
_DRIVER_YEARS = {
    "max verstappen":       [("toro rosso",2015,2015),("red bull",2016,2026)],
    "charles leclerc":      [("sauber",2018,2018),("ferrari",2019,2026)],
    "lewis hamilton":       [("mclaren",2007,2012),("mercedes",2013,2024),("ferrari",2025,2026)],
    "george russell":       [("williams",2019,2021),("mercedes",2022,2026)],
    "lando norris":         [("mclaren",2019,2026)],
    "oscar piastri":        [("mclaren",2023,2026)],
    "carlos sainz":         [("toro rosso",2015,2017),("renault",2018,2018),("mclaren",2019,2020),("ferrari",2021,2024),("williams",2025,2026)],
    "fernando alonso":      [("minardi",2001,2001),("renault",2003,2006),("mclaren",2007,2007),("renault",2008,2009),("ferrari",2010,2014),("mclaren",2015,2017),("alpine",2021,2022),("aston martin",2023,2026)],
    "lance stroll":         [("williams",2017,2018),("racing point",2019,2020),("aston martin",2021,2026)],
    "nico hulkenberg":      [("williams",2010,2010),("force india",2011,2012),("sauber",2013,2013),("force india",2014,2016),("renault",2017,2019),("racing point",2020,2020),("haas",2023,2026)],
    "pierre gasly":         [("toro rosso",2017,2017),("red bull",2019,2019),("toro rosso",2019,2019),("alphatauri",2020,2022),("alpine",2023,2026)],
    "esteban ocon":         [("manor",2016,2016),("force india",2017,2018),("renault",2019,2019),("alpine",2020,2023),("haas",2024,2026)],
    "valtteri bottas":      [("williams",2013,2016),("mercedes",2017,2021),("alfa romeo",2022,2023),("sauber",2024,2024),("cadillac",2026,2026)],
    "yuki tsunoda":         [("alphatauri",2021,2023),("racing bulls",2024,2025),("red bull",2025,2026)],
    "liam lawson":          [("alphatauri",2023,2023),("racing bulls",2024,2024),("red bull",2025,2026)],
    "alexander albon":      [("toro rosso",2019,2019),("red bull",2019,2020),("williams",2022,2026)],
    "oliver bearman":       [("ferrari",2024,2024),("haas",2025,2026)],
    "kimi antonelli":       [("mercedes",2025,2026)],
    "isack hadjar":         [("racing bulls",2025,2026)],
    "gabriel bortoleto":    [("sauber",2025,2026)],
    "jack doohan":          [("alpine",2025,2025)],
    "franco colapinto":     [("williams",2024,2024),("alpine",2025,2026)],
    "sebastian vettel":     [("bmw sauber",2007,2007),("toro rosso",2007,2009),("red bull",2009,2014),("ferrari",2015,2020),("aston martin",2021,2022)],
    "kimi raikkonen":       [("sauber",2001,2001),("mclaren",2002,2006),("ferrari",2007,2009),("lotus",2012,2013),("ferrari",2014,2018),("alfa romeo",2019,2021)],
    "jenson button":        [("williams",2000,2000),("benetton",2001,2001),("renault",2002,2002),("bar",2003,2005),("honda",2006,2008),("brawn gp",2009,2009),("mclaren",2010,2016)],
    "nico rosberg":         [("williams",2006,2009),("mercedes",2010,2016)],
    "daniel ricciardo":     [("hrt",2011,2011),("toro rosso",2012,2013),("red bull",2014,2018),("renault",2019,2020),("mclaren",2021,2022),("alphatauri",2023,2023),("racing bulls",2024,2024)],
    "sergio perez":         [("sauber",2011,2011),("mclaren",2013,2013),("force india",2014,2018),("racing point",2019,2020),("red bull",2021,2024),("cadillac",2026,2026)],
    "felipe massa":         [("sauber",2002,2002),("ferrari",2006,2013),("williams",2014,2017)],
    "romain grosjean":      [("renault",2009,2009),("lotus",2012,2015),("haas",2016,2020)],
    "stoffel vandoorne":    [("mclaren",2017,2018)],
    "daniil kvyat":         [("toro rosso",2014,2014),("red bull",2015,2016),("toro rosso",2016,2017),("toro rosso",2019,2020)],
    "kevin magnussen":      [("mclaren",2014,2014),("renault",2016,2016),("haas",2017,2020),("haas",2022,2024)],
    "marcus ericsson":      [("caterham",2014,2014),("sauber",2015,2018)],
    "pastor maldonado":     [("williams",2011,2013),("lotus",2014,2015)],
    "paul di resta":        [("force india",2011,2013)],
    "heikki kovalainen":    [("renault",2007,2007),("mclaren",2008,2009),("lotus",2010,2011),("caterham",2012,2013)],
    "jarno trulli":         [("minardi",1997,1997),("prost",1997,1999),("jordan",2000,2001),("renault",2002,2004),("toyota",2004,2009),("lotus",2010,2011)],
    "giancarlo fisichella": [("minardi",1996,1996),("jordan",1997,1997),("benetton",1998,2001),("jordan",2002,2002),("sauber",2003,2004),("renault",2004,2007),("force india",2008,2009),("ferrari",2009,2009)],
    "robert kubica":        [("bmw sauber",2006,2009),("lotus",2010,2010),("williams",2019,2019)],
    "nick heidfeld":        [("prost",2000,2000),("sauber",2001,2003),("jordan",2004,2004),("williams",2005,2005),("bmw sauber",2006,2009),("mercedes",2010,2010),("renault",2011,2011)],
    "rubens barrichello":   [("jordan",1993,1996),("stewart",1997,1999),("ferrari",2000,2005),("honda",2006,2008),("brawn gp",2009,2009),("williams",2010,2011)],
    "michael schumacher":   [("jordan",1991,1991),("benetton",1991,1995),("ferrari",1996,2006),("mercedes",2010,2012)],
    "mika hakkinen":        [("lotus",1991,1992),("mclaren",1993,2001)],
    "david coulthard":      [("williams",1994,1995),("mclaren",1996,2004),("red bull",2005,2008)],
    "eddie irvine":         [("jordan",1993,1995),("ferrari",1996,1999),("jaguar",2000,2002)],
    "heinz-harold frentzen":[("sauber",1994,1996),("williams",1997,1998),("jordan",1999,2001),("prost",2001,2001),("arrows",2002,2002)],
    "ralf schumacher":      [("jordan",1997,1998),("williams",1999,2004),("toyota",2005,2007)],
    "damon hill":           [("williams",1993,1996),("arrows",1997,1997),("jordan",1998,1999)],
    "nigel mansell":        [("lotus",1980,1984),("williams",1985,1988),("ferrari",1989,1990),("williams",1991,1992),("williams",1994,1994),("mclaren",1995,1995)],
    "ayrton senna":         [("toleman",1984,1984),("lotus",1985,1987),("mclaren",1988,1992),("williams",1994,1994)],
    "alain prost":          [("mclaren",1980,1980),("renault",1981,1983),("mclaren",1984,1989),("ferrari",1990,1991),("williams",1993,1993)],
    "nelson piquet":        [("ensign",1978,1978),("brabham",1978,1985),("williams",1986,1987),("lotus",1988,1989),("benetton",1990,1991)],
    "gerhard berger":       [("ats",1984,1984),("arrows",1985,1985),("benetton",1986,1986),("ferrari",1987,1989),("mclaren",1990,1992),("ferrari",1993,1995),("benetton",1996,1997)],
    "niki lauda":           [("march",1971,1972),("brm",1973,1973),("ferrari",1974,1977),("brabham",1978,1979),("mclaren",1982,1985)],
    "carlos reutemann":     [("brabham",1972,1976),("ferrari",1977,1978),("lotus",1979,1979),("williams",1980,1982)],
    "jody scheckter":       [("mclaren",1972,1972),("tyrrell",1974,1976),("wolf",1977,1978),("ferrari",1979,1980)],
    "james hunt":           [("hesketh",1973,1975),("mclaren",1976,1978),("wolf",1979,1979)],
    "mario andretti":       [("lotus",1976,1979),("alfa romeo",1981,1982)],
    "gilles villeneuve":    [("mclaren",1977,1977),("ferrari",1977,1982)],
    "emerson fittipaldi":   [("lotus",1970,1973),("mclaren",1974,1975),("fittipaldi",1976,1980)],
    "jackie stewart":       [("brm",1965,1967),("matra",1968,1969),("march",1970,1970),("tyrrell",1970,1973)],
    "clay regazzoni":       [("ferrari",1970,1972),("ferrari",1974,1976),("ensign",1977,1977),("shadow",1977,1977),("williams",1979,1979),("ensign",1980,1980)],
    "ronnie peterson":      [("march",1970,1972),("lotus",1973,1974),("march",1976,1976),("tyrrell",1977,1977),("lotus",1978,1978)],
    "jochen rindt":         [("cooper",1965,1967),("brabham",1968,1968),("lotus",1969,1970)],
    "jim clark":            [("lotus",1960,1968)],
    "juan manuel fangio":   [("alfa romeo",1950,1951),("maserati",1953,1953),("mercedes",1954,1955),("ferrari",1956,1956),("maserati",1957,1958)],
    "jack brabham":         [("cooper",1955,1960),("brabham",1962,1970)],
    "stirling moss":        [("maserati",1954,1956),("mercedes",1955,1955),("vanwall",1957,1958),("cooper",1959,1961),("lotus",1960,1962)],
    "john surtees":         [("lotus",1960,1960),("cooper",1960,1961),("ferrari",1963,1966),("honda",1967,1967),("surtees",1970,1972)],
    "graham hill":          [("lotus",1958,1959),("brm",1960,1966),("lotus",1967,1970),("brabham",1971,1972),("shadow",1973,1973)],
    "bruce mclaren":        [("cooper",1959,1965),("mclaren",1966,1970)],
    "denny hulme":          [("brabham",1965,1967),("mclaren",1968,1974)],
    "john watson":          [("brabham",1974,1975),("penske",1976,1977),("brabham",1977,1977),("mclaren",1979,1983)],
    "alan jones":           [("williams",1977,1981),("arrows",1983,1983)],
    "keke rosberg":         [("wolf",1978,1978),("fittipaldi",1979,1980),("williams",1982,1985),("mclaren",1986,1986)],
    "michele alboreto":     [("tyrrell",1981,1983),("ferrari",1984,1988),("tyrrell",1989,1989),("arrows",1990,1991)],
    "stefan johansson":     [("tyrrell",1983,1983),("toleman",1984,1984),("ferrari",1985,1986),("mclaren",1987,1988),("ligier",1988,1988)],
    "derek warwick":        [("toleman",1983,1984),("renault",1984,1985),("brabham",1986,1986),("arrows",1987,1988),("lotus",1990,1990)],
    "nelson piquet jr":     [("renault",2008,2009)],
    "mark webber":          [("minardi",2002,2002),("jaguar",2003,2004),("williams",2005,2006),("red bull",2007,2013)],
    "timo glock":           [("jordan",2004,2004),("toyota",2008,2009),("marussia",2010,2013)],
    "kamui kobayashi":      [("toyota",2009,2009),("sauber",2010,2012),("caterham",2014,2014)],
    "jean alesi":           [("tyrrell",1989,1990),("ferrari",1991,1995),("benetton",1996,1996),("sauber",1997,1998),("arrows",1999,1999),("prost",2000,2001),("jordan",2001,2001)],
    "olivier panis":        [("ligier",1994,1996),("prost",1997,1999),("bar",2001,2003),("toyota",2003,2004)],
    "mika salo":            [("lotus",1994,1994),("tyrrell",1995,1997),("arrows",1998,1998),("ferrari",1999,1999),("sauber",2000,2000),("toyota",2002,2002)],
    "johnny herbert":       [("benetton",1989,1989),("lotus",1990,1992),("lotus",1994,1994),("benetton",1994,1995),("sauber",1996,1998),("stewart",1999,1999),("jaguar",2000,2000)],
    "jj lehto":             [("onyx",1989,1989),("dallara",1991,1991),("sauber",1991,1993),("benetton",1994,1994)],
    "eddie cheever":        [("tyrrell",1978,1978),("ligier",1979,1979),("renault",1980,1982),("alfa romeo",1984,1985),("arrows",1986,1989)],
    "thierry boutsen":      [("arrows",1983,1985),("benetton",1986,1987),("williams",1989,1990),("ligier",1991,1992),("jordan",1993,1993)],
    "andrea de cesaris":    [("mclaren",1981,1981),("alfa romeo",1982,1983),("ligier",1984,1984),("minardi",1985,1986),("brabham",1986,1987),("rial",1988,1988),("dallara",1989,1990),("jordan",1991,1991),("tyrrell",1992,1994)],
    "martin brundle":       [("tyrrell",1984,1984),("zakspeed",1987,1987),("brabham",1989,1989),("williams",1992,1992),("benetton",1992,1993),("mclaren",1994,1994),("ligier",1995,1995),("jordan",1996,1996)],
    "jos verstappen":       [("benetton",1994,1994),("simtek",1995,1995),("footwork",1996,1996),("tyrrell",1997,1997),("stewart",1998,1998),("arrows",1999,2001),("minardi",2003,2003)],
    "johnny cecotto":       [("toleman",1983,1984)],
    "heikki kovalainen":    [("renault",2007,2007),("mclaren",2008,2009),("lotus",2010,2011),("caterham",2012,2013)],
    "tarso marques":        [("minardi",1996,1997),("minardi",2001,2001)],
    "luca badoer":          [("footwork",1993,1993),("minardi",1995,1996),("ferrari",1999,2000),("ferrari",2009,2009)],
    "ivan capelli":         [("tyrrell",1983,1983),("march",1987,1991),("ferrari",1992,1992),("jordan",1993,1993)],
    "alexander wurz":       [("benetton",1997,1999),("mclaren",2000,2000),("williams",2007,2007)],
    "rene arnoux":          [("renault",1979,1982),("ferrari",1983,1985),("ligier",1986,1989)],
    "patrick tambay":       [("mclaren",1978,1979),("ferrari",1982,1983),("renault",1984,1985)],
    "arturo merzario":      [("ferrari",1972,1973),("williams",1975,1975),("march",1978,1978)],
    "patrick depailler":    [("tyrrell",1972,1978),("ligier",1979,1979),("alfa romeo",1980,1980)],
    "didier pironi":        [("tyrrell",1978,1979),("ligier",1980,1980),("ferrari",1981,1982)],
    "elio de angelis":      [("shadow",1979,1979),("lotus",1980,1985),("brabham",1986,1986)],
    "riccardo patrese":     [("shadow",1977,1977),("arrows",1978,1981),("brabham",1982,1983),("alfa romeo",1985,1985),("brabham",1986,1987),("williams",1988,1992),("benetton",1993,1993)],
    "jean-pierre jabouille": [("renault",1977,1980)],
    "jacques villeneuve":   [("williams",1996,1998),("bar",1999,2003),("renault",2004,2004),("sauber",2005,2005),("bmw sauber",2006,2006)],
    "bertrand gachot":      [("onyx",1989,1989),("coloni",1990,1990),("jordan",1991,1991),("larrousse",1991,1992),("pacific",1994,1995)],
    "antonio giovinazzi":   [("sauber",2017,2017),("alfa romeo",2019,2021)],
    "guanyu zhou":          [("alfa romeo",2022,2023),("sauber",2024,2024)],
    "nyck de vries":        [("williams",2022,2022),("alphatauri",2023,2023)],
    "mick schumacher":      [("haas",2021,2022)],
    "nikita mazepin":       [("haas",2021,2021)],
    "vitaly petrov":        [("renault",2010,2011),("caterham",2012,2012)],
    "pedro de la rosa":     [("arrows",1999,2000),("jaguar",2002,2002),("mclaren",2005,2010),("sauber",2010,2010),("hrt",2011,2012),("williams",2012,2012)],
    "juan pablo montoya":   [("williams",2001,2004),("mclaren",2005,2006)],
    "scott speed":          [("toro rosso",2006,2007)],
    "sebastien buemi":      [("toro rosso",2009,2011)],
    "jaime alguersuari":    [("toro rosso",2009,2011)],
    "jean-eric vergne":     [("toro rosso",2012,2014)],
    "sebastien bourdais":   [("toro rosso",2008,2009)],
    "brendon hartley":      [("toro rosso",2017,2018)],
    "adrian sutil":         [("spyker",2007,2007),("force india",2008,2011),("force india",2013,2013),("sauber",2014,2014)],
    "jochen mass":          [("surtees",1973,1974),("mclaren",1974,1977),("arrows",1979,1982)],
    "chris amon":           [("lotus",1963,1963),("ferrari",1967,1969),("march",1970,1970),("matra",1971,1972),("tyrrell",1973,1973)],
    "piero taruffi":        [("alfa romeo",1950,1952),("ferrari",1952,1956)],
    "jacky ickx":           [("ferrari",1968,1969),("brabham",1969,1969),("ferrari",1970,1973),("lotus",1974,1975)],
    "henri pescarolo":      [("matra",1968,1971),("march",1972,1973),("brabham",1974,1974)],
    "francois cevert":      [("tyrrell",1970,1973)],
    "peter revson":         [("mclaren",1972,1973)],
    "jo siffert":           [("cooper",1963,1967),("lotus",1969,1969),("brm",1971,1971)],
    "pedro rodriguez":      [("ferrari",1965,1965),("cooper",1966,1968),("brm",1968,1971)],
    "dan gurney":           [("ferrari",1959,1959),("brm",1960,1960),("porsche",1961,1962),("brabham",1963,1965),("eagle",1966,1968)],
    "innes ireland":        [("lotus",1959,1962)],
    "tony brooks":          [("vanwall",1957,1958),("ferrari",1959,1959),("cooper",1960,1960),("brm",1960,1960)],
    "phill hill":           [("ferrari",1958,1962)],
    "alberto ascari":       [("ferrari",1950,1953),("lancia",1954,1955)],
    "giuseppe farina":      [("alfa romeo",1950,1951),("ferrari",1952,1955)],
    "luigi fagioli":        [("alfa romeo",1950,1951)],
    "mike hawthorn":        [("ferrari",1953,1955),("ferrari",1957,1958)],
    "peter collins":        [("ferrari",1956,1958)],
    "roy salvadori":        [("cooper",1958,1961),("aston martin",1961,1961)],
    "luigi musso":          [("ferrari",1956,1958)],
    "wolfgang von trips":   [("ferrari",1956,1961)],
    "richie ginther":       [("ferrari",1960,1961),("brm",1962,1964),("honda",1965,1966)],
    "jo bonnier":           [("brm",1959,1960),("porsche",1961,1962),("cooper",1963,1964)],
    "lorenzo bandini":      [("ferrari",1961,1961),("ferrari",1963,1967)],
    "bruce mclaren":        [("cooper",1959,1965),("mclaren",1966,1970)],
    "mike spence":          [("lotus",1963,1968)],
    "piers courage":        [("williams",1969,1970)],
    "gunnar nilsson":       [("lotus",1976,1977)],
    "lella lombardi":       [("march",1975,1975)],
    "jean-pierre beltoise": [("matra",1967,1971),("brm",1972,1974)],
    "vittorio brambilla":   [("march",1974,1977)],
    "bruno giacomelli":     [("alfa romeo",1978,1982)],
    "jan lammers":          [("shadow",1979,1979)],
    "philippe alliot":      [("ram",1984,1985),("larrousse",1986,1989)],
    "aguri suzuki":         [("larrousse",1990,1992),("footwork",1993,1993),("ligier",1994,1994)],
    "satoru nakajima":      [("lotus",1987,1989),("tyrrell",1991,1991)],
    "jean-pierre jabouille":[("renault",1977,1980)],
    "marc surer":           [("ensign",1979,1979),("ats",1980,1981),("arrows",1982,1985),("brabham",1985,1985)],
    "pierluigi martini":    [("minardi",1985,1992),("minardi",1994,1995)],
    "ukyo katayama":        [("tyrrell",1992,1995)],
    "narain karthikeyan":   [("jordan",2005,2005),("hrt",2011,2012)],
    "takuma sato":          [("bar",2002,2005),("super aguri",2006,2008)],
    "anthony davidson":     [("bar",2002,2003),("super aguri",2007,2008)],
    "vitantonio liuzzi":    [("red bull",2005,2005),("toro rosso",2006,2007),("force india",2009,2010),("hrt",2011,2011)],
    "christijan albers":    [("minardi",2005,2005),("spyker",2007,2007)],
    "mark webber":          [("minardi",2002,2002),("jaguar",2003,2004),("williams",2005,2006),("red bull",2007,2013)],
    "christian klien":      [("jaguar",2004,2004),("red bull",2005,2006),("spyker",2007,2007)],
    "tiago monteiro":       [("jordan",2005,2005)],
    "robert doornbos":      [("minardi",2005,2005),("red bull",2006,2006)],
    "marc gene":            [("minardi",1999,1999),("minardi",2000,2001),("williams",2003,2004),("ferrari",2003,2004)],
    "esteban gutierrez":    [("sauber",2012,2014),("haas",2016,2016)],
    "bruno senna":          [("hrt",2010,2011),("renault",2011,2011),("williams",2012,2012)],
    "pascal wehrlein":      [("manor",2016,2016),("sauber",2017,2017)],
    "nicholas latifi":      [("williams",2020,2022)],
    "logan sargeant":       [("williams",2023,2024)],
    "nyck de vries":        [("williams",2022,2022),("alphatauri",2023,2023)],
    "pierre gasly":         [("toro rosso",2017,2017),("red bull",2019,2019),("toro rosso",2019,2019),("alphatauri",2020,2022),("alpine",2023,2026)],
    "jack brabham":         [("cooper",1955,1960),("brabham",1962,1970)],
    "stirling moss":        [("maserati",1954,1956),("mercedes",1955,1955),("vanwall",1957,1958),("cooper",1959,1961),("lotus",1960,1962)],
    "juan manuel fangio":   [("alfa romeo",1950,1951),("maserati",1953,1953),("mercedes",1954,1955),("ferrari",1956,1956),("maserati",1957,1958)],
    "jose froilan gonzalez":[("ferrari",1951,1954),("maserati",1955,1957)],
    "mick schumacher":      [("haas",2021,2022)],
    "pietro fittipaldi":    [("haas",2020,2020)],
    "rio haryanto":         [("manor",2016,2016)],
    "will stevens":         [("caterham",2014,2014),("manor",2015,2015)],
    "jules bianchi":        [("marussia",2013,2014)],
    "max chilton":          [("marussia",2013,2014)],
    "charles pic":          [("marussia",2012,2012),("caterham",2013,2013)],
    "giedo van der garde":  [("caterham",2013,2013)],
    "lucas di grassi":      [("virgin",2010,2010)],
    "roberto merhi":        [("manor",2015,2015)],
    "jordan king":          [("manor",2016,2016)],
    "alexander rossi":      [("manor",2015,2015)],
    "harry schell":         [("maserati",1954,1955),("vanwall",1956,1957),("cooper",1958,1960)],
    "jose froilan gonzalez":[("ferrari",1951,1954),("maserati",1955,1957)],
    "hans joachim stuck":   [("march",1974,1974),("brabham",1974,1975),("shadow",1977,1978),("ats",1978,1979),("williams",1983,1985)],
    "teo fabi":             [("toleman",1982,1982),("brabham",1984,1984),("benetton",1987,1987)],
    "jean marc gounon":     [("minardi",1993,1993),("simtek",1994,1994)],
    "denny hulme":          [("brabham",1965,1967),("mclaren",1968,1974)],
    "jochen mass":          [("surtees",1973,1974),("mclaren",1974,1977),("arrows",1979,1982)],
    "stefan bellof":        [("tyrrell",1984,1985)],
    "jonathan palmer":      [("ram",1983,1984),("zakspeed",1987,1987),("tyrrell",1987,1989)],
    "christian danner":     [("zakspeed",1985,1985),("arrows",1986,1986),("rial",1988,1989)],
    "yannick dalmas":       [("larrousse",1987,1987),("ags",1988,1989),("coloni",1989,1989)],
    "emmanuele pirro":      [("benetton",1989,1989),("dallara",1990,1991)],
    "alex caffi":           [("osella",1986,1988),("dallara",1988,1990),("arrows",1990,1991)],
    "pedro paulo diniz":    [("forti",1995,1995),("ligier",1996,1996),("arrows",1997,1998),("sauber",1999,2000)],
    "antonio pizzonia":     [("jaguar",2003,2003),("williams",2003,2004),("bmw sauber",2005,2005)],
    "enrique bernoldi":     [("arrows",2001,2002)],
    "erik comas":           [("ligier",1991,1992),("larrousse",1993,1994)],
    "ralph firman":         [("jordan",2003,2003)],
    "zsolt baumgartner":    [("jordan",2003,2003),("minardi",2004,2004)],
    "hector rebaque":       [("lotus",1979,1980),("brabham",1980,1981)],
    "shinji nakano":        [("prost",1997,1997),("minardi",1998,1998)],
    "jan magnussen":        [("stewart",1997,1997)],
    "sakon yamamoto":       [("super aguri",2006,2006),("spyker",2007,2007)],
    "markus winkelhock":    [("spyker",2007,2007)],
    "helmut marko":         [("brm",1971,1972)],
    "howden ganley":        [("brm",1971,1972),("march",1973,1974)],
    "henri pescarolo":      [("matra",1968,1971),("march",1972,1973),("brabham",1974,1974)],
    "giancarlo baghetti":   [("ferrari",1961,1962)],
    "trevor taylor":        [("lotus",1961,1964)],
    "emilio de villota":    [("williams",1977,1977),("march",1977,1977)],
    "jean-eric vergne":     [("toro rosso",2012,2014)],
    "nick de vries":        [("williams",2022,2022),("alphatauri",2023,2023)],
    "jack fairman":         [("cooper",1958,1961)],
    "bob anderson":         [("lotus",1963,1963)],
}

def _build_chain_graph():
    """Construye el grafo de compañeros REALES usando años solapados."""
    from collections import defaultdict

    # Para cada equipo y año, lista de pilotos activos ese año en ese equipo
    # Primero expandimos _DRIVER_YEARS a (piloto, equipo, año) triples
    entries = []
    for driver, stints in _DRIVER_YEARS.items():
        for team, y1, y2 in stints:
            for yr in range(y1, y2 + 1):
                entries.append((driver, team, yr))

    # Agrupar por (equipo, año)
    from collections import defaultdict
    slot = defaultdict(list)
    for driver, team, yr in entries:
        slot[(team, yr)].append(driver)

    # Conectar compañeros reales
    graph      = defaultdict(set)
    team_graph = defaultdict(lambda: defaultdict(set))
    for (team, yr), drivers in slot.items():
        for i, a in enumerate(drivers):
            for b in drivers[i+1:]:
                if a != b:
                    graph[a].add(b)
                    graph[b].add(a)
                    team_graph[a][b].add((team, yr))
                    team_graph[b][a].add((team, yr))

    return dict(graph), {k: dict(v) for k, v in team_graph.items()}

_CHAIN_GRAPH, _CHAIN_TEAM_GRAPH = _build_chain_graph()

CHAIN_POOL = sorted(
    d for d in _CHAIN_GRAPH
    if d in SERIES_F1.drivers_meta and (
        SERIES_F1.drivers_meta[d]["wins"] > 0 or
        SERIES_F1.drivers_meta[d]["podiums"] >= 3
    )
)

def _chain_bfs(start, end):
    from collections import deque
    if start == end: return [start]
    visited = {start: None}
    queue = deque([start])
    while queue:
        node = queue.popleft()
        for nb in _CHAIN_GRAPH.get(node, set()):
            if nb not in visited:
                visited[nb] = node
                if nb == end:
                    path = []; cur = end
                    while cur: path.append(cur); cur = visited[cur]
                    return list(reversed(path))
                queue.append(nb)
    return None

def _chain_teams_between(a, b):
    """Devuelve lista de strings 'Equipo (año)' donde a y b fueron compañeros."""
    pairs = sorted(_CHAIN_TEAM_GRAPH.get(a, {}).get(b, set()))
    # Agrupar por equipo, quedarnos con el primer año de cada equipo
    by_team = {}
    for team, yr in pairs:
        if team not in by_team:
            by_team[team] = yr
    return [f"{t} ({y})" for t, y in sorted(by_team.items())]

def _pick_chain_pair(min_hops=2, max_hops=4):
    for _ in range(500):
        a, b = random.sample(CHAIN_POOL, 2)
        path = _chain_bfs(a, b)
        if path and min_hops <= len(path)-1 <= max_hops:
            return a, b, path
    a, b = random.sample(CHAIN_POOL, 2)
    return a, b, _chain_bfs(a, b) or [a, b]

# ══════════════════════════════════════════════════════════════════


# ══════════════════════════════════════════════════════════════════
#  MODO 9 — CIRCUITOS F1
# ══════════════════════════════════════════════════════════════════
F1_CIRCUITS = {
    "monaco": {
        "display":   "Mónaco",
        "pais":      "Mónaco",
        "ciudad":    "Monte Carlo",
        "longitud":  3.337,
        "vueltas":   78,
        "primer_gp": 1950,
        "tipo":      "urbano",
        "caracteristicas": [
            "El circuito más lento del calendario",
            "Tiene un túnel en su trazado",
            "Las barreras están a centímetros del asfalto",
            "Pasar por aquí sin tocar las barreras es casi un milagro",
            "Celebrado en las calles de un principado",
            "Tiene el famoso hairpin de la Curva de la Rascasse",
        ],
        "record_piloto": "max verstappen",
        "record_año":    2023,
        "ganadores":     ["ayrton senna", "graham hill", "michael schumacher"],
        "apodo":         "La Joya de la Corona",
    },
    "monza": {
        "display":   "Monza",
        "pais":      "Italia",
        "ciudad":    "Monza",
        "longitud":  5.793,
        "vueltas":   53,
        "primer_gp": 1950,
        "tipo":      "permanente",
        "caracteristicas": [
            "Conocido como el Templo de la Velocidad",
            "Es uno de los circuitos más rápidos del calendario",
            "Las rectas largas hacen que la velocidad punta sea máxima",
            "Se encuentra dentro de un parque histórico",
            "El público tifosi es mundialmente famoso",
            "Tiene una chicane en la primera curva",
        ],
        "record_piloto": "rubens barrichello",
        "record_año":    2004,
        "ganadores":     ["michael schumacher", "lewis hamilton", "sebastian vettel"],
        "apodo":         "El Templo de la Velocidad",
    },
    "silverstone": {
        "display":   "Silverstone",
        "pais":      "Gran Bretaña",
        "ciudad":    "Northamptonshire",
        "longitud":  5.891,
        "vueltas":   52,
        "primer_gp": 1950,
        "tipo":      "permanente",
        "caracteristicas": [
            "Fue el escenario del primer Gran Premio de F1 de la historia",
            "Es una antigua base de la RAF",
            "Tiene la famosa curva de alta velocidad Copse",
            "La recta de Hangar es una de las más rápidas del mundo",
            "Copse, Maggots, Becketts forman uno de los mejores sectores del calendario",
            "El clima suele ser impredecible",
        ],
        "record_piloto": "max verstappen",
        "record_año":    2020,
        "ganadores":     ["lewis hamilton", "nigel mansell", "alain prost"],
        "apodo":         "El hogar del automovilismo",
    },
    "spa": {
        "display":   "Spa-Francorchamps",
        "pais":      "Bélgica",
        "ciudad":    "Stavelot",
        "longitud":  7.004,
        "vueltas":   44,
        "primer_gp": 1950,
        "tipo":      "permanente",
        "caracteristicas": [
            "Es el circuito más largo del calendario actual",
            "Tiene la famosa curva Eau Rouge/Raidillon a plena velocidad",
            "El clima cambia de sección a sección del circuito",
            "Puede llover en un sector y estar seco en otro",
            "Combina alta velocidad con secciones técnicas",
            "Considerado por muchos pilotos como el mejor circuito del mundo",
        ],
        "record_piloto": "valtteri bottas",
        "record_año":    2018,
        "ganadores":     ["michael schumacher", "ayrton senna", "sebastian vettel"],
        "apodo":         "El Circuito de los Faraones",
    },
    "suzuka": {
        "display":   "Suzuka",
        "pais":      "Japón",
        "ciudad":    "Suzuka",
        "longitud":  5.807,
        "vueltas":   53,
        "primer_gp": 1987,
        "tipo":      "permanente",
        "caracteristicas": [
            "Tiene un trazado en forma de ocho con un paso elevado",
            "La S de la primera chicane es icónica",
            "La curva 130R es una de las más rápidas del mundo",
            "Construido por Honda para probar sus autos",
            "Escenario de épicas batallas por el campeonato",
            "Tiene el famoso Degner Corner y el Casino Triangle",
        ],
        "record_piloto": "lewis hamilton",
        "record_año":    2019,
        "ganadores":     ["michael schumacher", "ayrton senna", "max verstappen"],
        "apodo":         "El Circuito del Ocho",
    },
    "interlagos": {
        "display":   "Interlagos",
        "pais":      "Brasil",
        "ciudad":    "São Paulo",
        "longitud":  4.309,
        "vueltas":   71,
        "primer_gp": 1973,
        "tipo":      "permanente",
        "caracteristicas": [
            "Se corre en sentido antihorario",
            "Tiene la famosa curva Senna S a la entrada",
            "El nombre significa 'entre lagos'",
            "Las lluvias tropicales son habituales en la carrera",
            "Tiene una recta de los boxes muy larga",
            "Escenario de muchos campeonatos decididos en la última vuelta",
        ],
        "record_piloto": "valtteri bottas",
        "record_año":    2018,
        "ganadores":     ["ayrton senna", "michael schumacher", "lewis hamilton"],
        "apodo":         "La Catedral del Automovilismo Brasileño",
    },
    "barcelona": {
        "display":   "Barcelona",
        "pais":      "España",
        "ciudad":    "Montmeló",
        "longitud":  4.657,
        "vueltas":   66,
        "primer_gp": 1991,
        "tipo":      "permanente",
        "caracteristicas": [
            "Es la sede habitual de los test de pretemporada",
            "Los pilotos lo conocen de memoria por los test",
            "La curva Campsa ofrece gran espectáculo",
            "Tiene una larga recta principal para adelantamientos",
            "El asfalto se degrada mucho en el sector medio",
            "La curva 3 Nissan fue rediseñada para facilitar adelantamientos",
        ],
        "record_piloto": "max verstappen",
        "record_año":    2023,
        "ganadores":     ["michael schumacher", "lewis hamilton", "max verstappen"],
        "apodo":         "El Laboratorio",
    },
    "abu dhabi": {
        "display":   "Abu Dhabi",
        "pais":      "Emiratos Árabes",
        "ciudad":    "Abu Dhabi",
        "longitud":  5.281,
        "vueltas":   58,
        "primer_gp": 2009,
        "tipo":      "semipermanente",
        "caracteristicas": [
            "La carrera empieza de día y termina de noche",
            "Se encuentra en la isla artificial de Yas Marina",
            "Tiene un hotel de lujo integrado en el trazado",
            "Es la última carrera del calendario desde 2009",
            "Fue rediseñado en 2021 para facilitar adelantamientos",
            "El hotel Yas Viceroy fue parte icónica del trazado original",
        ],
        "record_piloto": "max verstappen",
        "record_año":    2021,
        "ganadores":     ["sebastian vettel", "lewis hamilton", "max verstappen"],
        "apodo":         "La Pista del Amanecer al Atardecer",
    },
    "budapest": {
        "display":   "Hungaroring",
        "pais":      "Hungría",
        "ciudad":    "Budapest",
        "longitud":  4.381,
        "vueltas":   70,
        "primer_gp": 1986,
        "tipo":      "permanente",
        "caracteristicas": [
            "Fue el primer GP detrás del Telón de Acero",
            "Es conocido por ser muy difícil para adelantar",
            "El clima húmedo en agosto suele sorprender",
            "La curva 4 tiene la mejor zona de frenada del circuito",
            "El agarre suele ser muy bajo fuera de la línea de carrera",
            "Se parece a Mónaco sin barreras, según los pilotos",
        ],
        "record_piloto": "lewis hamilton",
        "record_año":    2020,
        "ganadores":     ["ayrton senna", "michael schumacher", "lewis hamilton"],
        "apodo":         "El Mónaco del Este",
    },
    "zandvoort": {
        "display":   "Zandvoort",
        "pais":      "Países Bajos",
        "ciudad":    "Zandvoort",
        "longitud":  4.259,
        "vueltas":   72,
        "primer_gp": 1952,
        "tipo":      "permanente",
        "caracteristicas": [
            "Tiene peraltes extremos en sus curvas lentas",
            "Volvió al calendario en 2021 tras 35 años de ausencia",
            "Está rodeado de dunas de arena",
            "El público naranja holandés llena las gradas",
            "Fue rediseñado con bancos elevados tipo NASCAR",
            "La curva Hugenholtz es la más famosa del trazado",
        ],
        "record_piloto": "max verstappen",
        "record_año":    2023,
        "ganadores":     ["niki lauda", "james hunt", "max verstappen"],
        "apodo":         "La Catedral Naranja",
    },
    "imola": {
        "display":   "Imola",
        "pais":      "Italia",
        "ciudad":    "Imola",
        "longitud":  4.909,
        "vueltas":   63,
        "primer_gp": 1980,
        "tipo":      "permanente",
        "caracteristicas": [
            "Es el único circuito con dos nombres de santos en su nombre oficial",
            "Escenario de la tragedia de Senna en 1994",
            "Tiene la famosa curva Tamburello, hoy una chicane",
            "Volvió al calendario en 2020 tras 14 años de ausencia",
            "La zona de boxes está al final de la recta principal",
            "El circuito se llama Enzo e Dino Ferrari",
        ],
        "record_piloto": "rubens barrichello",
        "record_año":    2004,
        "ganadores":     ["ayrton senna", "michael schumacher", "max verstappen"],
        "apodo":         "El Circuito de Senna",
    },
    "singapore": {
        "display":   "Singapur",
        "pais":      "Singapur",
        "ciudad":    "Marina Bay",
        "longitud":  5.063,
        "vueltas":   62,
        "primer_gp": 2008,
        "tipo":      "urbano",
        "caracteristicas": [
            "Primer Gran Premio nocturno de la historia de F1",
            "Se corre completamente de noche bajo miles de focos",
            "El calor y la humedad son extremos para los pilotos",
            "Tiene más de 20 curvas y pocas rectas largas",
            "Pasa por el centro financiero de la ciudad",
            "El Safety Car aparece con mucha frecuencia aquí",
        ],
        "record_piloto": "kevin magnussen",
        "record_año":    2018,
        "ganadores":     ["sebastian vettel", "lewis hamilton", "carlos sainz"],
        "apodo":         "La Carrera Nocturna",
    },
    "baku": {
        "display":   "Bakú",
        "pais":      "Azerbaiyán",
        "ciudad":    "Bakú",
        "longitud":  6.003,
        "vueltas":   51,
        "primer_gp": 2016,
        "tipo":      "urbano",
        "caracteristicas": [
            "Tiene la segunda recta más larga del calendario",
            "Pasa por la Ciudad Vieja declarada Patrimonio de la Humanidad",
            "El tramo del castillo es increíblemente estrecho",
            "Los pinchazos en la última vuelta son famosos aquí",
            "Los Safety Cars son muy frecuentes en este circuito",
            "La recta principal supera los 340 km/h de velocidad punta",
        ],
        "record_piloto": "charles leclerc",
        "record_año":    2019,
        "ganadores":     ["nico rosberg", "sergio perez", "max verstappen"],
        "apodo":         "La Pista del Caos",
    },
    "montreal": {
        "display":   "Montreal",
        "pais":      "Canadá",
        "ciudad":    "Montreal",
        "longitud":  4.361,
        "vueltas":   70,
        "primer_gp": 1978,
        "tipo":      "semipermanente",
        "caracteristicas": [
            "Se encuentra en la Isla Notre-Dame, artificial",
            "Tiene la famosa Muralla de los Campeones al final",
            "Es un circuito stop-and-go con frenadas muy duras",
            "El DRS es muy efectivo en su larga recta principal",
            "Lleva el nombre de un piloto local icónico",
            "El muro exterior del último chicane ha destruido muchas carreras",
        ],
        "record_piloto": "valtteri bottas",
        "record_año":    2019,
        "ganadores":     ["michael schumacher", "lewis hamilton", "ayrton senna"],
        "apodo":         "El Circuito Gilles Villeneuve",
    },
    "nurburgring": {
        "display":   "Nürburgring",
        "pais":      "Alemania",
        "ciudad":    "Nürburg",
        "longitud":  5.148,
        "vueltas":   60,
        "primer_gp": 1951,
        "tipo":      "permanente",
        "caracteristicas": [
            "El circuito moderno se llama GP-Strecke",
            "El antiguo Nordschleife tiene 20 km y es el más peligroso del mundo",
            "Escenario del famoso accidente y recuperación de Niki Lauda en 1976",
            "El clima aquí es absolutamente impredecible",
            "Schumacher fue campeón aquí con Ferrari varias veces",
            "Fue llamado el Infierno Verde por los pilotos clásicos",
        ],
        "record_piloto": "michael schumacher",
        "record_año":    2004,
        "ganadores":     ["michael schumacher", "lewis hamilton", "sebastian vettel"],
        "apodo":         "El Infierno Verde",
    },
    "jeddah": {
        "display":   "Jeddah",
        "pais":      "Arabia Saudí",
        "ciudad":    "Jeddah",
        "longitud":  6.174,
        "vueltas":   50,
        "primer_gp": 2021,
        "tipo":      "urbano",
        "caracteristicas": [
            "Es el circuito urbano más rápido del calendario",
            "Tiene más de 27 curvas, casi todas en rápido",
            "Las barreras están muy cerca de la pista",
            "Visibilidad reducida por las curvas ciegas encadenadas",
            "Las velocidades puntas superan los 330 km/h",
            "Se inauguró en 2021 para el penúltimo GP de ese año",
        ],
        "record_piloto": "lewis hamilton",
        "record_año":    2021,
        "ganadores":     ["lewis hamilton", "max verstappen", "sergio perez"],
        "apodo":         "La Autopista de Arabia",
    },
    "bahrain": {
        "display":   "Bahréin",
        "pais":      "Bahréin",
        "ciudad":    "Sakhir",
        "longitud":  5.412,
        "vueltas":   57,
        "primer_gp": 2004,
        "tipo":      "permanente",
        "caracteristicas": [
            "Fue el primer Gran Premio en Oriente Medio",
            "La carrera nocturna crea un espectáculo visual único",
            "El polvo del desierto suele irrumpir en la pista",
            "Tiene una variante oval que se usó en 2020 como Sakhir GP",
            "La zona de frenada de la curva 1 genera muchos adelantamientos",
            "El asfalto abrasivo destruye los neumáticos con rapidez",
        ],
        "record_piloto": "pedro de la rosa",
        "record_año":    2005,
        "ganadores":     ["michael schumacher", "lewis hamilton", "sebastian vettel"],
        "apodo":         "La Perla del Golfo",
    },
    "melbourne": {
        "display":   "Melbourne",
        "pais":      "Australia",
        "ciudad":    "Melbourne",
        "longitud":  5.278,
        "vueltas":   58,
        "primer_gp": 1996,
        "tipo":      "semipermanente",
        "caracteristicas": [
            "Suele ser la primera carrera de la temporada",
            "El asfalto nuevo al inicio del año da poca adherencia",
            "Hay muchos Safety Cars en la primera vuelta",
            "Se corre alrededor del lago Albert Park",
            "El público australiano es muy festivo y ruidoso",
            "Las calles se usan normalmente para el tráfico cotidiano",
        ],
        "record_piloto": "charles leclerc",
        "record_año":    2022,
        "ganadores":     ["michael schumacher", "damon hill", "lewis hamilton"],
        "apodo":         "El Albert Park",
    },
    "shanghai": {
        "display":   "Shanghai",
        "pais":      "China",
        "ciudad":    "Shanghai",
        "longitud":  5.451,
        "vueltas":   56,
        "primer_gp": 2004,
        "tipo":      "permanente",
        "caracteristicas": [
            "Tiene la curva de apertura más larga del calendario",
            "La curva 1-2 es un caracol descendente que dura varios segundos",
            "Fue diseñado por Hermann Tilke",
            "El sector final tiene una recta muy larga para DRS",
            "Volvió al calendario en 2024 tras años de ausencia",
            "La infraestructura del paddock es una de las más modernas",
        ],
        "record_piloto": "michael schumacher",
        "record_año":    2004,
        "ganadores":     ["michael schumacher", "lewis hamilton", "nico rosberg"],
        "apodo":         "El Caracol",
    },
    "austin": {
        "display":   "Austin (COTA)",
        "pais":      "Estados Unidos",
        "ciudad":    "Austin, Texas",
        "longitud":  5.513,
        "vueltas":   56,
        "primer_gp": 2012,
        "tipo":      "permanente",
        "caracteristicas": [
            "Las siglas COTA significan Circuit of the Americas",
            "Fue diseñado con inspiración en los mejores circuitos del mundo",
            "La curva 1 es una de las subidas más espectaculares del calendario",
            "Tiene el sector inspirado en Maggots y Becketts de Silverstone",
            "Lewis Hamilton ganó aquí una cantidad histórica de veces",
            "El terreno texano permite grandes cambios de elevación",
        ],
        "record_piloto": "charles leclerc",
        "record_año":    2019,
        "ganadores":     ["lewis hamilton", "sebastian vettel", "max verstappen"],
        "apodo":         "El Circuito de las Américas",
    },
    "mexico": {
        "display":   "México",
        "pais":      "México",
        "ciudad":    "Ciudad de México",
        "longitud":  4.304,
        "vueltas":   71,
        "primer_gp": 1963,
        "tipo":      "permanente",
        "caracteristicas": [
            "Es el circuito a mayor altitud del calendario: 2200 metros sobre el nivel del mar",
            "La delgadez del aire afecta el motor y la aerodinámica",
            "Los frenos duran más por la menor resistencia del aire",
            "El estadio al final del circuito crea un ambiente único",
            "El público mexicano es uno de los más apasionados del mundo",
            "Los equipos deben reconfigurar el auto para la altitud",
        ],
        "record_piloto": "valtteri bottas",
        "record_año":    2021,
        "ganadores":     ["nigel mansell", "max verstappen", "lewis hamilton"],
        "apodo":         "El Estadio de la Fórmula 1",
    },
    "las vegas": {
        "display":   "Las Vegas",
        "pais":      "Estados Unidos",
        "ciudad":    "Las Vegas",
        "longitud":  6.201,
        "vueltas":   50,
        "primer_gp": 2023,
        "tipo":      "urbano",
        "caracteristicas": [
            "La recta del Strip pasa frente a los casinos más famosos del mundo",
            "La carrera se corre de madrugada hora local",
            "El frío nocturno del desierto complica el calentamiento de neumáticos",
            "Es uno de los circuitos más rápidos por las rectas largas",
            "Tiene el Caesars Palace y el Bellagio en el trazado",
            "Fue la gran apuesta de F1 para crecer en el mercado americano",
        ],
        "record_piloto": "oscar piastri",
        "record_año":    2024,
        "ganadores":     ["max verstappen", "carlos sainz"],
        "apodo":         "La Carrera del Strip",
    },
    "qatar": {
        "display":   "Catar",
        "pais":      "Catar",
        "ciudad":    "Losail",
        "longitud":  5.380,
        "vueltas":   57,
        "primer_gp": 2021,
        "tipo":      "permanente",
        "caracteristicas": [
            "Originalmente era un circuito de MotoGP",
            "Tiene muchas curvas rápidas encadenadas sin mucha frenada",
            "El calor extremo es el mayor enemigo de pilotos y neumáticos",
            "Se corre de noche para evitar el calor diurno",
            "Las degradaciones de neumáticos son brutales aquí",
            "El Losail Circuit fue construido en tiempo récord",
        ],
        "record_piloto": "max verstappen",
        "record_año":    2023,
        "ganadores":     ["lewis hamilton", "max verstappen", "george russell"],
        "apodo":         "El Horno del Desierto",
    },
    "miami": {
        "display":   "Miami",
        "pais":      "Estados Unidos",
        "ciudad":    "Miami Gardens",
        "longitud":  5.412,
        "vueltas":   57,
        "primer_gp": 2022,
        "tipo":      "semipermanente",
        "caracteristicas": [
            "Se corre alrededor del estadio del equipo de fútbol americano Miami Dolphins",
            "Tiene un lago artificial en el paddock que no lleva agua real",
            "Fue construido en tiempo récord para la temporada 2022",
            "Las curvas 14-16 son el sector más técnico del trazado",
            "El calor y la humedad de Florida afectan mucho el rendimiento",
            "El ambiente festivo y colorido es único en el calendario",
        ],
        "record_piloto": "max verstappen",
        "record_año":    2023,
        "ganadores":     ["max verstappen", "lando norris"],
        "apodo":         "El Hard Rock Stadium Circuit",
    },
}

