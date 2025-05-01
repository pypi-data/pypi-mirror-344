from saved_instance.db.sqllite_repo import SqliteRepo
from saved_instance.rich_storage import RichStorage

def test_rich_test_storage():
    repo: SqliteRepo = SqliteRepo("rich_test_storage.db")
    rs = RichStorage(repo)
    # rs["dict"] = {"1": 1, "2": {"3": 3}}
    # rs["dict"]["2"]["3"] = "hey"
    # rs["test"] = {"1": 1, "2":
    #                         {"3":
    #                              {"4": 4
    #
    #                               }
    #                          }
    #               }
    # print(pd)
    # pd["1"] = 2
    # print(pd)
    # print(rs["dict"]["1"])
    # rs["test"]["2"]["3"]["4"] = {"5": 5}
    # rs["test"]["2"]["3"]["4"]["5"] = "hi"
    # rs.update({"test": "2"})
    # print(rs["test"])

    #1
    # rs["list_test"] = []
    # rs["list_test"].append(1)
    # print(rs["list_test"])

    #2
    # rs["list_test"] = {"1": []}
    # rs["list_test"]["1"].append(1)
    # print(rs["list_test"])

    #2
    # rs["list_test"] = {"1": [], "2": {"3": []}}
    # val = rs["list_test"]["2"]["3"]
    # print(val)
    # val.append(3)
    # print(rs["list_test"])

    #3
    # rs["list_test"] = {"1": [{"2":2}]}
    # print(type(rs["list_test"]["1"][0]))
    # rs["list_test"]["1"][0]["2"] = 3
    # print(rs["list_test"])

    #4
    # rs["list_test"] = {"1": [], "2": {"3": [{"5":5}]}}
    # val = rs["list_test"]["2"]["3"][0]
    # val["5"] = 6
    # print(rs["list_test"])

    #5
    # rs["list_test"] = {"1": [{"2":2}, 1]}
    # rs["list_test"]["1"][1] = 3
    # print(rs["list_test"])

    #6
    rs["list_test"] = {"1": [{"2":2}, {"3": [0,1,2]}]}
    rs["list_test"]["1"][1]["3"][1] = 3
    print(rs["list_test"])
    assert rs["list_test"] == {"1": [{"2":2}, {"3": [0,3,2]}]}

    # for key, item in rs.items():
    #     print(key, item)
