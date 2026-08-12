from ingest import chunk_document, load_documents


def test_load_documents_uses_lab_directory_from_any_working_directory(
    monkeypatch, tmp_path
):
    monkeypatch.chdir(tmp_path)

    documents = load_documents()

    assert len(documents) == 8
    assert documents[0]["game"] == "Catan"
    assert all(document["text"] for document in documents)


def test_chunk_document_preserves_overlap_and_metadata():
    text = "".join(str(index % 10) for index in range(600))

    chunks = chunk_document(text, "Ticket To Ride")

    assert [chunk["chunk_id"] for chunk in chunks] == [
        "ticket_to_ride_0",
        "ticket_to_ride_1",
        "ticket_to_ride_2",
    ]
    assert all(chunk["game"] == "Ticket To Ride" for chunk in chunks)
    assert chunks[0]["text"][-50:] == chunks[1]["text"][:50]
    assert chunks[1]["text"][-50:] == chunks[2]["text"][:50]


def test_chunk_document_drops_short_input():
    assert chunk_document("Too short", "Catan") == []
