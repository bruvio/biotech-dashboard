# from src.app import server
from src.utils.data import get_data


def test_index(client):

    res = client.get("/")
    assert res.status_code == 200


def test_read():

    assay, ic50, labels, df = get_data()

    assert assay is not None
    assert ic50 is not None
    assert labels is not None
    assert df is not None


def test_size_df():
    assay, ic50, labels, df = get_data()

    assert (
        len(ic50["Compound ID"].unique())
        == len(labels["Compound ID"].unique())
        == len(assay["Compound ID"].unique())
        == len(df["ID"].unique())
    )
