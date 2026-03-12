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
        "Gran Premio de Gran Bretaña":  ["giuseppe farina","luigi fagioli","reg parnell","yves giraud-cabantous","louis rosier","johnnie claes","juan manuel fangio","prince bira","david murray","toulo de graffenried"],
        "Gran Premio de Mónaco":        ["juan manuel fangio","alberto ascari","luigi villoresi","louis chiron","jose froilan gonzalez","juan manuel fangio","louis rosier","robert manzon","raymond sommer","prince bira"],
        "Gran Premio de Suiza":         ["giuseppe farina","luigi fagioli","louis rosier","prince bira","toulo de graffenried","juan manuel fangio","jose froilan gonzalez","dorino serafini","peter whitehead","eugene martin"],
    },
    1951: {
        "Gran Premio de Gran Bretaña":  ["jose froilan gonzalez","juan manuel fangio","luigi villoresi","piero taruffi","felice bonetto","reg parnell","bob gerard","juan manuel fangio","alberto ascari","stirling moss"],
        "Gran Premio de España":        ["juan manuel fangio","jose froilan gonzalez","giuseppe farina","alberto ascari","luigi villoresi","juan manuel fangio","piero taruffi","luigi fagioli","roberto mieres","emmanuel de graffenried"],
    },
    1952: {
        "Gran Premio de Gran Bretaña":  ["alberto ascari","piero taruffi","jose froilan gonzalez","mike hawthorn","dennis poore","eric thompson","giuseppe farina","robert manzon","jean behra","alan brown"],
        "Gran Premio de Italia":        ["alberto ascari","jose froilan gonzalez","luigi villoresi","giuseppe farina","mike hawthorn","piero taruffi","alan brown","eric thompson","jim mayers","peter whitehead"],
    },
    1953: {
        "Gran Premio de Argentina":     ["alberto ascari","luigi villoresi","jose froilan gonzalez","mike hawthorn","oscar galvez","frolian gonzalez","juan manuel fangio","piero taruffi","giuseppe farina","nino farina"],
        "Gran Premio de Gran Bretaña":  ["alberto ascari","juan manuel fangio","jose froilan gonzalez","mike hawthorn","giuseppe farina","luigi villoresi","piero taruffi","stirling moss","reg parnell","sergio mantovani"],
    },
    # ── Años 60 ───────────────────────────────────────────────────
    1961: {
        "Gran Premio de Mónaco":        ["stirling moss","richie ginther","phil hill","dan gurney","bruce mclaren","graham hill","innes ireland","jim clark","tony brooks","jo bonnier"],
        "Gran Premio de Italia":        ["phil hill","dan gurney","richie ginther","giancarlo baghetti","innes ireland","jack brabham","bruce mclaren","graham hill","jo bonnier","ron flockhart"],
    },
    1963: {
        "Gran Premio de Mónaco":        ["graham hill","richie ginther","bruce mclaren","jack brabham","innes ireland","tony maggs","trevor taylor","jo bonnier","carel godin de beaufort","masten gregory"],
        "Gran Premio de Italia":        ["jim clark","richie ginther","bruce mclaren","innes ireland","jack brabham","graham hill","jo siffert","tony maggs","jo bonnier","mike spence"],
    },
    1965: {
        "Gran Premio de Mónaco":        ["graham hill","lorenzo bandini","jackie stewart","john surtees","richie ginther","bruce mclaren","bob bondurant","innes ireland","jo siffert","denny hulme"],
        "Gran Premio de Gran Bretaña":  ["jim clark","john surtees","graham hill","mike spence","jackie stewart","denny hulme","bob bondurant","jackie stewart","richie ginther","innes ireland"],
        "Gran Premio de Italia":        ["jackie stewart","graham hill","dan gurney","lorenzo bandini","denny hulme","richie ginther","jo siffert","bruce mclaren","jackie stewart","bob bondurant"],
    },
    1967: {
        "Gran Premio de Mónaco":        ["denny hulme","graham hill","chris amon","pedro rodriguez","mike parkes","bob anderson","ricarda rodriguez","piers courage","bruce mclaren","jo siffert"],
        "Gran Premio de Gran Bretaña":  ["jim clark","denny hulme","chris amon","jack brabham","pedro rodriguez","graham hill","dan gurney","jo siffert","chris irwin","piers courage"],
        "Gran Premio de Italia":        ["john surtees","jack brabham","jim clark","jochen rindt","mike spence","dan gurney","jacky ickx","brian redman","chris amon","jo siffert"],
    },
    1968: {
        "Gran Premio de Mónaco":        ["graham hill","richard attwood","lucien bianchi","loouis chiron","jacky ickx","brian redman","dan gurney","chris amon","jo siffert","denny hulme"],
        "Gran Premio de Gran Bretaña":  ["jo siffert","chris amon","jacky ickx","denny hulme","jack brabham","graham hill","dan gurney","brian redman","piers courage","pete lovely"],
    },
    1969: {
        "Gran Premio de Mónaco":        ["graham hill","piers courage","jo siffert","brian redman","denny hulme","richard attwood","vic elford","jacky ickx","bruce mclaren","john surtees"],
        "Gran Premio de Gran Bretaña":  ["jacky ickx","jack brabham","jochen rindt","bruce mclaren","john surtees","piers courage","vicc elford","graham hill","jo siffert","denny hulme"],
    },
    # ── Años 70 ───────────────────────────────────────────────────
    1970: {
        "Gran Premio de Mónaco":        ["jochen rindt","jack brabham","henri pescarolo","denny hulme","rolf stommelen","pedro rodriguez","jacky ickx","graham hill","amos posey","pete lovely"],
        "Gran Premio de Italia":        ["clay regazzoni","jacky ickx","denny hulme","rolf stommelen","francois cevert","jochen rindt","graham hill","pedro rodriguez","john miles","andrea de adamich"],
        "Gran Premio de Austria":       ["jacky ickx","clay regazzoni","denny hulme","rolf stommelen","jochen rindt","emerson fittipaldi","jo siffert","pedro rodriguez","derek bell","graham hill"],
    },
    1971: {
        "Gran Premio de Mónaco":        ["jackie stewart","ronnie peterson","emerson fittipaldi","jacky ickx","denny hulme","clay regazzoni","mario andretti","graham hill","rolf stommelen","pedro rodriguez"],
        "Gran Premio de Italia":        ["peter gethin","ronnie peterson","francois cevert","mike hailwood","howden ganley","clay regazzoni","chris amon","jo siffert","rolf stommelen","graham hill"],
    },
    1973: {
        "Gran Premio de Mónaco":        ["jackie stewart","emerson fittipaldi","ronnie peterson","francois cevert","denny hulme","mike hailwood","carlos reutemann","jean-pierre beltoise","peter revson","clay regazzoni"],
        "Gran Premio de Gran Bretaña":  ["peter revson","ronnie peterson","denny hulme","james hunt","jackie oliver","carlos reutemann","jackie stewart","andrea de cesaris","jody scheckter","arturo merzario"],
        "Gran Premio de Italia":        ["ronnie peterson","emerson fittipaldi","peter revson","jackie stewart","francois cevert","carlos reutemann","denny hulme","jody scheckter","arturo merzario","andrea de cesaris"],
    },
    1975: {
        "Gran Premio de Mónaco":        ["niki lauda","emerson fittipaldi","carlos reutemann","jochen mass","patrick depailler","mike hailwood","vittorio brambilla","jody scheckter","ronnie peterson","clay regazzoni"],
        "Gran Premio de Gran Bretaña":  ["emerson fittipaldi","carlos reutemann","jody scheckter","jochen mass","patricio depailler","niki lauda","james hunt","clay regazzoni","mario andretti","ronnie peterson"],
        "Gran Premio de Nürburgring":   ["carlos reutemann","jochen mass","niki lauda","james hunt","patrick depailler","jody scheckter","tony brise","clay regazzoni","ronnie peterson","lella lombardi"],
    },
    1976: {
        "Gran Premio de Mónaco":        ["niki lauda","jody scheckter","patrick depailler","hans joachim stuck","jochen mass","emerson fittipaldi","clay regazzoni","james hunt","rolf stommelen","jacky ickx"],
        "Gran Premio de Gran Bretaña":  ["james hunt","niki lauda","jody scheckter","jochen mass","carlos reutemann","hans joachim stuck","tom pryce","alan jones","emerson fittipaldi","ronnie peterson"],
        "Gran Premio de Japón":         ["mario andretti","jody scheckter","james hunt","patrick depailler","alan jones","gunnar nilsson","clay regazzoni","masahiro hasemi","niki lauda","vittorio brambilla"],
    },
    1977: {
        "Gran Premio de Mónaco":        ["jody scheckter","niki lauda","carlos reutemann","jochen mass","mario andretti","gunnar nilsson","john watson","alan jones","rupert keegan","brett lunger"],
        "Gran Premio de Gran Bretaña":  ["james hunt","niki lauda","gunnar nilsson","jochen mass","alan jones","hans joachim stuck","david purley","patrick depailler","clay regazzoni","jean-pierre jarier"],
    },
    1978: {
        "Gran Premio de Mónaco":        ["patrick depailler","niki lauda","jody scheckter","carlos reutemann","mario andretti","jacky ickx","gilles villeneuve","nelson piquet","jo siffert","derek daly"],
        "Gran Premio de Gran Bretaña":  ["carlos reutemann","niki lauda","john watson","jochen mass","mario andretti","hans joachim stuck","james hunt","alan jones","hector rebaque","derek daly"],
        "Gran Premio de Italia":        ["mario andretti","gilles villeneuve","ronnie peterson","jody scheckter","niki lauda","john watson","carlos reutemann","derek daly","vittorio brambilla","riccardo patrese"],
    },
    1979: {
        "Gran Premio de Mónaco":        ["jody scheckter","clay regazzoni","carlos reutemann","john watson","patrick depailler","jochen mass","gilles villeneuve","alan jones","derek daly","mario andretti"],
        "Gran Premio de Gran Bretaña":  ["clay regazzoni","rene arnoux","jean-pierre jarier","john watson","jochen mass","carlos reutemann","mario andretti","nelson piquet","daly derek","jacky ickx"],
        "Gran Premio de Francia":       ["jean-pierre jabouille","gilles villeneuve","rene arnoux","alan jones","jody scheckter","clay regazzoni","john watson","mario andretti","carlos reutemann","jochen mass"],
    },
    1984: {
        "Gran Premio de Mónaco":       ["alain prost","ayrton senna","stefan bellof","rene arnoux","keke rosberg","michele alboreto","nigel mansell","niki lauda","derek bell","jonathan palmer"],
        "Gran Premio de Gran Bretaña": ["niki lauda","derek warwick","ayrton senna","elio de angelis","jonathan palmer","nigel mansell","alain prost","jacques laffite","niki lauda","martin brundle"],
    },
    1986: {
        "Gran Premio de Australia":    ["alain prost","nelson piquet","stefan johansson","martin brundle","philippe streiff","thierry boutsen","philippe alliot","christian danner","alan jones","gerhard berger"],
        "Gran Premio de San Marino":   ["alain prost","nelson piquet","gerhard berger","stefan johansson","riccardo patrese","andrea de cesaris","derek warwick","christian danner","jonathan palmer","thierry boutsen"],
    },
    1988: {
        "Gran Premio de Mónaco":       ["ayrton senna","alain prost","gerhard berger","michele alboreto","thierry boutsen","derek warwick","bernd schneider","stefano modena","alex caffi","pierluigi martini"],
        "Gran Premio de Gran Bretaña": ["ayrton senna","nigel mansell","alain prost","martin brundle","gerhard berger","stefan johansson","nelson piquet","derek warwick","thierry boutsen","mauricio gugelmin"],
        "Gran Premio de Hungría":      ["ayrton senna","alain prost","thierry boutsen","gerhard berger","derek warwick","riccardo patrese","mauricio gugelmin","ivan capelli","pierluigi martini","nelson piquet"],
        "Gran Premio de Italia":       ["gerhard berger","michele alboreto","eddie cheever","derek warwick","thierry boutsen","riccardo patrese","andrea de cesaris","pierluigi martini","jonathan palmer","alex caffi"],
    },
    1989: {
        "Gran Premio de Gran Bretaña": ["alain prost","nigel mansell","ayrton senna","gerhard berger","nelson piquet","thierry boutsen","stefano modena","christian danner","derek warwick","pierluigi martini"],
        "Gran Premio de Mónaco":       ["ayrton senna","alain prost","stefano modena","nigel mansell","eddie cheever","riccardo patrese","gerhard berger","nelson piquet","emanuele pirro","oscar larrauri"],
    },
    1990: {
        "Gran Premio de Mónaco":       ["ayrton senna","jean alesi","gerhard berger","thierry boutsen","roberto moreno","aguri suzuki","derek warwick","eric bernard","stefan johansson","alex caffi"],
        "Gran Premio de Japón":        ["nelson piquet","roberto moreno","aguri suzuki","thierry boutsen","nigel mansell","jean alesi","riccardo patrese","derek warwick","alain prost","stefano modena"],
    },
    1991: {
        "Gran Premio de Gran Bretaña": ["nigel mansell","gerhard berger","alain prost","ayrton senna","michael schumacher","bertrand gachot","roberto moreno","mark blundell","ivan capelli","j.j. lehto"],
        "Gran Premio de Mónaco":       ["ayrton senna","nigel mansell","jean alesi","roberto moreno","stefano modena","bertrand gachot","j.j. lehto","eric bernard","pierluigi martini","emanuele pirro"],
        "Gran Premio de San Marino":   ["ayrton senna","gerhard berger","j.j. lehto","riccardo patrese","martin brundle","jean alesi","pierluigi martini","bertrand gachot","roberto moreno","aguri suzuki"],
    },
    1992: {
        "Gran Premio de Gran Bretaña": ["nigel mansell","riccardo patrese","martin brundle","michael schumacher","gerhard berger","ayrton senna","mika hakkinen","thierry boutsen","bertrand gachot","jean alesi"],
        "Gran Premio de Hungría":      ["ayrton senna","nigel mansell","gerhard berger","michael schumacher","martin brundle","jean alesi","thierry boutsen","johnny herbert","bertrand gachot","ivan capelli"],
        "Gran Premio de Bélgica":      ["michael schumacher","nigel mansell","riccardo patrese","ayrton senna","martin brundle","gerhard berger","mika hakkinen","erik comas","thierry boutsen","jean alesi"],
    },
    1993: {
        "Gran Premio de Gran Bretaña": ["alain prost","michael schumacher","mark blundell","riccardo patrese","johnny herbert","martin brundle","rubens barrichello","derek warwick","christian fittipaldi","aguri suzuki"],
        "Gran Premio de Mónaco":       ["ayrton senna","damon hill","jean alesi","michael andretti","martin brundle","johnny herbert","mark blundell","derek warwick","christian fittipaldi","philippe alliot"],
        "Gran Premio de Europa":       ["ayrton senna","alain prost","damon hill","michael schumacher","jean alesi","karl wendlinger","mika hakkinen","rubens barrichello","derek warwick","christian fittipaldi"],
    },
    1994: {
        "Gran Premio de Gran Bretaña": ["damon hill","michael schumacher","mika hakkinen","jos verstappen","martin brundle","david coulthard","olivier panis","christian fittipaldi","rubens barrichello","eric bernard"],
        "Gran Premio de Hungría":      ["michael schumacher","damon hill","jos verstappen","martin brundle","olivier panis","eric bernard","andrea montermini","mika salo","david coulthard","heinz-harold frentzen"],
        "Gran Premio de Australia":    ["nigel mansell","gerhard berger","martin brundle","rubens barrichello","mika hakkinen","olivier panis","gianni morbidelli","damon hill","aguri suzuki","david coulthard"],
    },
    1995: {
        "Gran Premio de Gran Bretaña": ["johnny herbert","jean alesi","damon hill","olivier panis","mika hakkinen","gerhard berger","rubens barrichello","mark blundell","karl wendlinger","mika salo"],
        "Gran Premio de Mónaco":       ["michael schumacher","damon hill","gerhard berger","jean alesi","johnny herbert","heinz-harold frentzen","mika hakkinen","olivier panis","mark blundell","mika salo"],
        "Gran Premio de Italia":       ["johnny herbert","mika hakkinen","heinz-harold frentzen","martin brundle","gerhard berger","jean alesi","rubens barrichello","olivier panis","gianni morbidelli","andrea montermini"],
    },
    1996: {
        "Gran Premio de Gran Bretaña": ["jacques villeneuve","gerhard berger","mika hakkinen","damon hill","david coulthard","rubens barrichello","eddie irvine","martin brundle","heinz-harold frentzen","jos verstappen"],
        "Gran Premio de Mónaco":       ["olivier panis","david coulthard","johnny herbert","heinz-harold frentzen","mika salo","michael schumacher","rubens barrichello","pedro diniz","mika hakkinen","jarno trulli"],
        "Gran Premio de Japón":        ["damon hill","michael schumacher","mika hakkinen","gerhard berger","mika salo","johnny herbert","rubens barrichello","eddie irvine","martin brundle","olivier panis"],
    },
    1997: {
        "Gran Premio de Mónaco":       ["michael schumacher","rubens barrichello","heinz-harold frentzen","eddie irvine","olivier panis","mika salo","jarno trulli","ralf schumacher","mika hakkinen","pedro diniz"],
        "Gran Premio de Gran Bretaña": ["michael schumacher","mika hakkinen","heinz-harold frentzen","gerhard berger","david coulthard","alexander wurz","ralf schumacher","jarno trulli","rubens barrichello","eddie irvine"],
        "Gran Premio de Hungría":      ["jacques villeneuve","damon hill","johnny herbert","ralf schumacher","michael schumacher","heinz-harold frentzen","mika hakkinen","rubens barrichello","shinji nakano","mika salo"],
    },
    1998: {
        "Gran Premio de Gran Bretaña": ["michael schumacher","mika hakkinen","eddie irvine","alexander wurz","damon hill","david coulthard","ralf schumacher","mika salo","heinz-harold frentzen","rubens barrichello"],
        "Gran Premio de Mónaco":       ["mika hakkinen","giancarlo fisichella","eddie irvine","mika salo","heinz-harold frentzen","damon hill","pedro diniz","jos verstappen","olivier panis","ralf schumacher"],
        "Gran Premio de Hungría":      ["michael schumacher","david coulthard","jacques villeneuve","damon hill","ralf schumacher","heinz-harold frentzen","giancarlo fisichella","alexander wurz","olivier panis","pedro diniz"],
        "Gran Premio de Japón":        ["mika hakkinen","eddie irvine","david coulthard","damon hill","heinz-harold frentzen","michael schumacher","rubens barrichello","jan magnussen","ralf schumacher","shinji nakano"],
    },
    1999: {
        "Gran Premio de Mónaco":       ["michael schumacher","eddie irvine","mika hakkinen","heinz-harold frentzen","ralf schumacher","giancarlo fisichella","alexander wurz","damon hill","pedro diniz","jarno trulli"],
        "Gran Premio de Gran Bretaña": ["david coulthard","eddie irvine","ralf schumacher","heinz-harold frentzen","damon hill","mika salo","jarno trulli","alexander wurz","olivier panis","pedro diniz"],
        "Gran Premio de Japón":        ["mika hakkinen","michael schumacher","eddie irvine","heinz-harold frentzen","ralf schumacher","johnny herbert","giancarlo fisichella","rubens barrichello","mika salo","alex zanardi"],
    },
    2000: {
        "Gran Premio de Mónaco":       ["david coulthard","rubens barrichello","giancarlo fisichella","michael schumacher","eddie irvine","jenson button","mika salo","heinz-harold frentzen","nick heidfeld","tarso marques"],
        "Gran Premio de Gran Bretaña": ["david coulthard","michael schumacher","rubens barrichello","mika hakkinen","heinz-harold frentzen","jenson button","ralf schumacher","eddie irvine","giancarlo fisichella","pedro diniz"],
        "Gran Premio de Italia":       ["michael schumacher","mika hakkinen","ralf schumacher","rubens barrichello","jenson button","heinz-harold frentzen","eddie irvine","giancarlo fisichella","mika salo","pedro diniz"],
        "Gran Premio de Japón":        ["michael schumacher","mika hakkinen","david coulthard","rubens barrichello","ralf schumacher","giancarlo fisichella","jenson button","nick heidfeld","heinz-harold frentzen","eddie irvine"],
    },
    2001: {
        "Gran Premio de Mónaco":       ["michael schumacher","david coulthard","rubens barrichello","eddie irvine","jarno trulli","jenson button","ralf schumacher","olivier panis","jean alesi","heinz-harold frentzen"],
        "Gran Premio de Gran Bretaña": ["mika hakkinen","michael schumacher","rubens barrichello","ralf schumacher","david coulthard","jarno trulli","mika salo","olivier panis","jean alesi","nick heidfeld"],
        "Gran Premio de Hungría":      ["michael schumacher","rubens barrichello","david coulthard","ralf schumacher","mika hakkinen","olivier panis","jean alesi","jenson button","jarno trulli","kimi raikkonen"],
    },
    2002: {
        "Gran Premio de Mónaco":       ["david coulthard","michael schumacher","ralf schumacher","jenson button","eddie irvine","rubens barrichello","jarno trulli","kimi raikkonen","nick heidfeld","olivier panis"],
        "Gran Premio de Gran Bretaña": ["michael schumacher","rubens barrichello","juan pablo montoya","david coulthard","ralf schumacher","kimi raikkonen","nick heidfeld","jenson button","jarno trulli","felipe massa"],
        "Gran Premio de Hungría":      ["rubens barrichello","michael schumacher","ralf schumacher","david coulthard","kimi raikkonen","jenson button","giancarlo fisichella","nick heidfeld","takuma sato","jarno trulli"],
    },
    2003: {
        "Gran Premio de Gran Bretaña": ["rubens barrichello","juan pablo montoya","kimi raikkonen","michael schumacher","ralf schumacher","david coulthard","jenson button","heinz-harold frentzen","mark webber","giancarlo fisichella"],
        "Gran Premio de Mónaco":       ["juan pablo montoya","kimi raikkonen","michael schumacher","ralf schumacher","jenson button","david coulthard","mark webber","jarno trulli","olivier panis","antonio pizzonia"],
        "Gran Premio de Hungría":      ["fernando alonso","kimi raikkonen","juan pablo montoya","jenson button","michael schumacher","mark webber","ralf schumacher","david coulthard","jarno trulli","giancarlo fisichella"],
        "Gran Premio de Italia":       ["michael schumacher","juan pablo montoya","rubens barrichello","jenson button","david coulthard","jarno trulli","giancarlo fisichella","ralph firman","antonio pizzonia","heinz-harold frentzen"],
    },
    2004: {
        "Gran Premio de Mónaco":       ["jarno trulli","jenson button","rubens barrichello","juan pablo montoya","michael schumacher","olivier panis","david coulthard","giancarlo fisichella","kimi raikkonen","antonio pizzonia"],
        "Gran Premio de Gran Bretaña": ["michael schumacher","kimi raikkonen","rubens barrichello","ralf schumacher","jenson button","juan pablo montoya","takuma sato","david coulthard","giancarlo fisichella","mark webber"],
        "Gran Premio de Hungría":      ["michael schumacher","rubens barrichello","david coulthard","kimi raikkonen","jenson button","ralf schumacher","takuma sato","giancarlo fisichella","antonio pizzonia","christian klien"],
        "Gran Premio de Japón":        ["michael schumacher","rubens barrichello","jenson button","david coulthard","takuma sato","mark webber","ralf schumacher","giancarlo fisichella","antonio pizzonia","christian klien"],
    },
    2005: {
        "Gran Premio de Mónaco":       ["nick heidfeld","mark webber","rubens barrichello","david coulthard","jenson button","antonio pizzonia","christian klien","narain karthikeyan","tiago monteiro","christijan albers"],
        "Gran Premio de Gran Bretaña": ["juan pablo montoya","fernando alonso","kimi raikkonen","michael schumacher","jenson button","rubens barrichello","ralf schumacher","giancarlo fisichella","mark webber","jarno trulli"],
        "Gran Premio de Hungría":      ["kimi raikkonen","michael schumacher","ralf schumacher","nick heidfeld","giancarlo fisichella","david coulthard","christijan albers","tiago monteiro","narain karthikeyan","robert doornbos"],
        "Gran Premio de Italia":       ["juan pablo montoya","kimi raikkonen","giancarlo fisichella","ralf schumacher","jenson button","michael schumacher","mark webber","christian klien","david coulthard","nick heidfeld"],
        "Gran Premio de Japón":        ["kimi raikkonen","giancarlo fisichella","ralf schumacher","jenson button","takuma sato","nick heidfeld","jarno trulli","christian klien","mark webber","narain karthikeyan"],
    },
    2006: {
        "Gran Premio de Mónaco":       ["david coulthard","michael schumacher","rubens barrichello","jenson button","mark webber","nico rosberg","tiago monteiro","christijan albers","narain karthikeyan","scott speed"],
        "Gran Premio de Italia":       ["michael schumacher","kimi raikkonen","nick heidfeld","jenson button","nico rosberg","robert kubica","ralf schumacher","jarno trulli","scott speed","christijan albers"],
        "Gran Premio de Japón":        ["michael schumacher","giancarlo fisichella","ralf schumacher","robert kubica","nico rosberg","nick heidfeld","jenson button","rubens barrichello","tiago monteiro","christian klien"],
    },
    2007: {
        "Gran Premio de Mónaco":       ["fernando alonso","lewis hamilton","felipe massa","mark webber","jenson button","giancarlo fisichella","nico rosberg","david coulthard","jarno trulli","heikki kovalainen"],
        "Gran Premio de Gran Bretaña": ["kimi raikkonen","lewis hamilton","nico rosberg","rubens barrichello","mark webber","nick heidfeld","fernando alonso","ralf schumacher","jenson button","heikki kovalainen"],
        "Gran Premio de Hungría":      ["lewis hamilton","kimi raikkonen","nick heidfeld","fernando alonso","heikki kovalainen","ralf schumacher","nico rosberg","giancarlo fisichella","jarno trulli","jenson button"],
        "Gran Premio de Italia":       ["fernando alonso","lewis hamilton","kimi raikkonen","nick heidfeld","robert kubica","nico rosberg","mark webber","ralf schumacher","alexander wurz","jenson button"],
        "Gran Premio de Japón":        ["lewis hamilton","heikki kovalainen","kimi raikkonen","fernando alonso","robert kubica","nick heidfeld","jenson button","mark webber","jarno trulli","giancarlo fisichella"],
    },
    2008: {
        "Gran Premio de Mónaco":       ["lewis hamilton","robert kubica","felipe massa","mark webber","nico rosberg","heikki kovalainen","david coulthard","sebastien bourdais","jarno trulli","jenson button"],
        "Gran Premio de Gran Bretaña": ["mark webber","nico rosberg","kimi raikkonen","lewis hamilton","nick heidfeld","jarno trulli","sebastien bourdais","timo glock","jenson button","heikki kovalainen"],
        "Gran Premio de Hungría":      ["heikki kovalainen","timo glock","kimi raikkonen","mark webber","lewis hamilton","nico rosberg","jarno trulli","nick heidfeld","sebastien bourdais","jenson button"],
        "Gran Premio de Italia":       ["sebastian vettel","heikki kovalainen","robert kubica","lewis hamilton","timo glock","kimi raikkonen","sebastien bourdais","mark webber","nick heidfeld","david coulthard"],
        "Gran Premio de Brasil":       ["felipe massa","lewis hamilton","kimi raikkonen","fernando alonso","sebastian vettel","mark webber","robert kubica","timo glock","heikki kovalainen","nico rosberg"],
    },
    2009: {
        "Gran Premio de Gran Bretaña": ["sebastian vettel","mark webber","rubens barrichello","jenson button","kimi raikkonen","heikki kovalainen","romain grosjean","nick heidfeld","timo glock","giancarlo fisichella"],
        "Gran Premio de Mónaco":       ["jenson button","rubens barrichello","kimi raikkonen","felipe massa","mark webber","nico rosberg","jarno trulli","timo glock","heikki kovalainen","romain grosjean"],
        "Gran Premio de Hungría":      ["lewis hamilton","kimi raikkonen","mark webber","heikki kovalainen","nico rosberg","romain grosjean","giancarlo fisichella","sebastian vettel","nick heidfeld","timo glock"],
        "Gran Premio de Japón":        ["sebastian vettel","jarno trulli","lewis hamilton","nick heidfeld","timo glock","heikki kovalainen","nico rosberg","rubens barrichello","kamui kobayashi","romain grosjean"],
        "Gran Premio de Abu Dabi":     ["sebastian vettel","mark webber","jenson button","rubens barrichello","kimi raikkonen","nico rosberg","timo glock","heikki kovalainen","giancarlo fisichella","romain grosjean"],
    },
    2010: {
        "Gran Premio de Gran Bretaña": ["mark webber","lewis hamilton","nico rosberg","rubens barrichello","adrian sutil","jenson button","heikki kovalainen","vitaly petrov","sebastien buemi","timo glock"],
        "Gran Premio de Mónaco":       ["mark webber","sebastian vettel","robert kubica","fernando alonso","michael schumacher","rubens barrichello","nico rosberg","jenson button","lewis hamilton","vitaly petrov"],
        "Gran Premio de Hungría":      ["mark webber","fernando alonso","sebastian vettel","jenson button","michael schumacher","robert kubica","nico rosberg","rubens barrichello","vitaly petrov","nick heidfeld"],
        "Gran Premio de Italia":       ["fernando alonso","jenson button","felipe massa","lewis hamilton","nico hulkenberg","michael schumacher","vitaly petrov","robert kubica","nick heidfeld","heikki kovalainen"],
        "Gran Premio de Abu Dabi":     ["sebastian vettel","lewis hamilton","jenson button","fernando alonso","michael schumacher","nico rosberg","vitaly petrov","robert kubica","adrian sutil","timo glock"],
    },
    2011: {
        "Gran Premio de Gran Bretaña": ["fernando alonso","sebastian vettel","mark webber","jenson button","felipe massa","nico rosberg","michael schumacher","lewis hamilton","paul di resta","vitaly petrov"],
        "Gran Premio de Mónaco":       ["sebastian vettel","mark webber","jenson button","fernando alonso","michael schumacher","david coulthard","nico rosberg","lewis hamilton","kamui kobayashi","jaime alguersuari"],
        "Gran Premio de Hungría":      ["jenson button","sebastian vettel","mark webber","fernando alonso","lewis hamilton","nico rosberg","michael schumacher","kamui kobayashi","jaime alguersuari","paul di resta"],
        "Gran Premio de Italia":       ["sebastian vettel","jenson button","fernando alonso","mark webber","nico rosberg","michael schumacher","jaime alguersuari","paul di resta","kamui kobayashi","vitaly petrov"],
        "Gran Premio de Japón":        ["jenson button","sebastian vettel","fernando alonso","mark webber","michael schumacher","nico rosberg","lewis hamilton","kamui kobayashi","jaime alguersuari","paul di resta"],
    },
    2012: {
        "Gran Premio de Gran Bretaña": ["mark webber","fernando alonso","sebastian vettel","nico rosberg","lewis hamilton","jenson button","kamui kobayashi","romain grosjean","michael schumacher","pablo maldonado"],
        "Gran Premio de Mónaco":       ["mark webber","nico rosberg","fernando alonso","michael schumacher","jenson button","romain grosjean","sebastian vettel","lewis hamilton","kamui kobayashi","paul di resta"],
        "Gran Premio de Hungría":      ["lewis hamilton","kimi raikkonen","romain grosjean","sebastian vettel","fernando alonso","mark webber","jenson button","nico rosberg","pastor maldonado","sergio perez"],
        "Gran Premio de Italia":       ["lewis hamilton","sebastian vettel","jenson button","felipe massa","nico rosberg","kimi raikkonen","michael schumacher","sergio perez","romain grosjean","mark webber"],
        "Gran Premio de Brasil":       ["jenson button","fernando alonso","felipe massa","sebastian vettel","nico hulkenberg","nico rosberg","kimi raikkonen","lewis hamilton","kamui kobayashi","pastor maldonado"],
    },
    2013: {
        "Gran Premio de Gran Bretaña": ["nico rosberg","mark webber","fernando alonso","sebastian vettel","kimi raikkonen","jenson button","romain grosjean","lewis hamilton","adrian sutil","pastor maldonado"],
        "Gran Premio de Mónaco":       ["nico rosberg","sebastian vettel","mark webber","lewis hamilton","felipe massa","romain grosjean","kimi raikkonen","daniel ricciardo","jean-eric vergne","sergio perez"],
        "Gran Premio de Hungría":      ["lewis hamilton","kimi raikkonen","sebastian vettel","romain grosjean","jenson button","mark webber","felipe massa","nico rosberg","sergio perez","daniel ricciardo"],
        "Gran Premio de Italia":       ["sebastian vettel","mark webber","lewis hamilton","kimi raikkonen","felipe massa","nico rosberg","jenson button","romain grosjean","jean-eric vergne","daniel ricciardo"],
    },
    2014: {
        "Gran Premio de Gran Bretaña": ["lewis hamilton","valtteri bottas","daniel ricciardo","nico rosberg","sebastian vettel","kevin magnussen","jenson button","sergio perez","nico hulkenberg","felipe massa"],
        "Gran Premio de Mónaco":       ["nico rosberg","lewis hamilton","daniel ricciardo","sebastian vettel","jenson button","romain grosjean","sergio perez","kevin magnussen","valtteri bottas","jean-eric vergne"],
        "Gran Premio de Hungría":      ["daniel ricciardo","fernando alonso","lewis hamilton","sebastian vettel","romain grosjean","jenson button","kevin magnussen","valtteri bottas","nico rosberg","sergio perez"],
        "Gran Premio de Italia":       ["lewis hamilton","nico rosberg","felipe massa","fernando alonso","sebastian vettel","jenson button","kevin magnussen","kimi raikkonen","valtteri bottas","sergio perez"],
        "Gran Premio de Abu Dabi":     ["lewis hamilton","felipe massa","valtteri bottas","jenson button","sebastian vettel","kevin magnussen","sergio perez","nico hulkenberg","romain grosjean","jean-eric vergne"],
    },
    2015: {
        "Gran Premio de Gran Bretaña": ["lewis hamilton","nico rosberg","sebastian vettel","romain grosjean","daniil kvyat","pastor maldonado","max verstappen","carlos sainz","jenson button","nico hulkenberg"],
        "Gran Premio de Mónaco":       ["nico rosberg","sebastian vettel","lewis hamilton","pastor maldonado","romain grosjean","daniil kvyat","sergio perez","max verstappen","carlos sainz","jenson button"],
        "Gran Premio de Hungría":      ["sebastian vettel","daniil kvyat","pastor maldonado","romain grosjean","sergio perez","max verstappen","nico rosberg","carlos sainz","jenson button","lewis hamilton"],
        "Gran Premio de Italia":       ["lewis hamilton","sebastian vettel","romain grosjean","valtteri bottas","nico rosberg","daniil kvyat","max verstappen","carlos sainz","pastor maldonado","sergio perez"],
        "Gran Premio de Japón":        ["lewis hamilton","nico rosberg","sebastian vettel","romain grosjean","valtteri bottas","daniil kvyat","sergio perez","max verstappen","pastor maldonado","carlos sainz"],
    },
    2016: {
        "Gran Premio de Gran Bretaña": ["lewis hamilton","max verstappen","nico rosberg","sergio perez","kimi raikkonen","romain grosjean","nico hulkenberg","valtteri bottas","daniil kvyat","carlos sainz"],
        "Gran Premio de Mónaco":       ["lewis hamilton","daniel ricciardo","sergio perez","sebastian vettel","jenson button","daniil kvyat","carlos sainz","valtteri bottas","romain grosjean","kevin magnussen"],
        "Gran Premio de España":       ["max verstappen","kimi raikkonen","sebastian vettel","carlos sainz","sergio perez","romain grosjean","daniil kvyat","nico hulkenberg","valtteri bottas","jenson button"],
        "Gran Premio de Bélgica":      ["nico rosberg","daniel ricciardo","romain grosjean","kimi raikkonen","sebastian vettel","max verstappen","nico hulkenberg","valtteri bottas","sergio perez","daniil kvyat"],
        "Gran Premio de Italia":       ["nico rosberg","sebastian vettel","kimi raikkonen","valtteri bottas","sergio perez","carlos sainz","nico hulkenberg","romain grosjean","daniil kvyat","kevin magnussen"],
        "Gran Premio de Abu Dabi":     ["lewis hamilton","nico rosberg","sebastian vettel","kimi raikkonen","valtteri bottas","max verstappen","sergio perez","carlos sainz","nico hulkenberg","esteban ocon"],
    },
    2017: {
        "Gran Premio de Gran Bretaña": ["lewis hamilton","valtteri bottas","kimi raikkonen","sebastian vettel","carlos sainz","max verstappen","lance stroll","esteban ocon","felipe massa","nico hulkenberg"],
        "Gran Premio de Mónaco":       ["sebastian vettel","kimi raikkonen","daniel ricciardo","carlos sainz","sergio perez","jenson button","lance stroll","esteban ocon","daniil kvyat","felipe massa"],
        "Gran Premio de España":       ["lewis hamilton","valtteri bottas","daniel ricciardo","sebastian vettel","kimi raikkonen","max verstappen","sergio perez","esteban ocon","carlos sainz","felipe massa"],
        "Gran Premio de Italia":       ["lewis hamilton","valtteri bottas","sebastian vettel","kimi raikkonen","max verstappen","esteban ocon","carlos sainz","nico hulkenberg","sergio perez","daniel ricciardo"],
        "Gran Premio de Japón":        ["lewis hamilton","max verstappen","sebastian vettel","esteban ocon","carlos sainz","valtteri bottas","sergio perez","kimi raikkonen","lance stroll","felipe massa"],
        "Gran Premio de Abu Dabi":     ["valtteri bottas","lewis hamilton","sebastian vettel","kimi raikkonen","max verstappen","sergio perez","esteban ocon","lance stroll","carlos sainz","nico hulkenberg"],
    },
    2018: {
        "Gran Premio de Gran Bretaña": ["sebastian vettel","lewis hamilton","kimi raikkonen","valtteri bottas","romain grosjean","kevin magnussen","esteban ocon","carlos sainz","fernando alonso","lance stroll"],
        "Gran Premio de Mónaco":       ["daniel ricciardo","sebastian vettel","lewis hamilton","kimi raikkonen","max verstappen","valtteri bottas","fernando alonso","carlos sainz","esteban ocon","nico hulkenberg"],
        "Gran Premio de Hungría":      ["lewis hamilton","sebastian vettel","kimi raikkonen","valtteri bottas","romain grosjean","carlos sainz","kevin magnussen","esteban ocon","max verstappen","charles leclerc"],
        "Gran Premio de Italia":       ["lewis hamilton","kimi raikkonen","valtteri bottas","romain grosjean","esteban ocon","kevin magnussen","carlos sainz","sebastian vettel","lance stroll","sergio perez"],
        "Gran Premio de Abu Dabi":     ["lewis hamilton","max verstappen","carlos sainz","valtteri bottas","sebastian vettel","kimi raikkonen","kevin magnussen","romain grosjean","fernando alonso","lance stroll"],
    },
    2019: {
        "Gran Premio de Gran Bretaña": ["valtteri bottas","lewis hamilton","charles leclerc","pierre gasly","sebastian vettel","carlos sainz","kevin magnussen","daniil kvyat","lando norris","lance stroll"],
        "Gran Premio de Mónaco":       ["lewis hamilton","sebastian vettel","max verstappen","charles leclerc","valtteri bottas","pierre gasly","carlos sainz","lando norris","nico hulkenberg","antonio giovinazzi"],
        "Gran Premio de España":       ["lewis hamilton","valtteri bottas","max verstappen","sebastian vettel","charles leclerc","pierre gasly","carlos sainz","kimi raikkonen","lando norris","kevin magnussen"],
        "Gran Premio de Italia":       ["charles leclerc","valtteri bottas","lewis hamilton","pierre gasly","carlos sainz","kimi raikkonen","lando norris","lance stroll","nico hulkenberg","antonio giovinazzi"],
        "Gran Premio de Brasil":       ["max verstappen","pierre gasly","carlos sainz","lewis hamilton","sebastian vettel","nico hulkenberg","valtteri bottas","lando norris","lance stroll","kevin magnussen"],
        "Gran Premio de Abu Dabi":     ["lewis hamilton","max verstappen","charles leclerc","sebastian vettel","valtteri bottas","pierre gasly","lando norris","carlos sainz","nico hulkenberg","daniil kvyat"],
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


