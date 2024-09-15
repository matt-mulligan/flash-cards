from pathlib import Path
from unittest.mock import ANY, Mock, call, patch

from flash_cards.orm import Game, Question, create_tables, get_questions, submit_game


@patch("flash_cards.orm.Base")
@patch("flash_cards.orm._get_engine")
def test_when_create_tables_and_no_db_path_then_correct_calls_made(get_engine, base):
    engine = Mock()
    get_engine.return_value = engine

    create_tables()

    get_engine.assert_called_once_with(None)
    base.assert_has_calls([call.metadata.create_all(bind=engine)])


@patch("flash_cards.orm.Base")
@patch("flash_cards.orm._get_engine")
def test_when_create_tables_and_db_path_then_correct_calls_made(get_engine, base):
    engine = Mock()
    get_engine.return_value = engine

    create_tables(db_path=Path("/my/database.sqlite"))

    get_engine.assert_called_once_with(Path("/my/database.sqlite"))
    base.assert_has_calls([call.metadata.create_all(bind=engine)])


@patch("flash_cards.orm.Session")
@patch("flash_cards.orm.select")
@patch("flash_cards.orm._get_engine")
def test_when_get_questions_and_no_question_set_then_correct_calls_made(get_engine, select, session_cls):
    question_a = Question()
    question_b = Question()
    question_c = Question()

    engine = Mock()
    session = Mock()
    session.__enter__ = Mock(return_value=session)
    session.__exit__ = Mock(return_value=None)
    session.scalars().all = Mock(return_value=[question_a, question_b, question_c])

    get_engine.return_value = engine
    session_cls.return_value = session

    actual = get_questions()

    assert actual == [question_a, question_b, question_c]

    get_engine.assert_called_once_with(None)
    select.assert_has_calls([call(Question)])
    session_cls.assert_called_once_with(engine)
    session.assert_has_calls(
        [
            call.scalars(select()),
            call.scalars().all(),
        ]
    )


@patch("flash_cards.orm.Session")
@patch("flash_cards.orm.select")
@patch("flash_cards.orm._get_engine")
def test_when_get_questions_and_question_set_then_correct_calls_made(get_engine, select, session_cls):
    question_a = Question()
    question_c = Question()

    engine = Mock()
    session = Mock()
    session.__enter__ = Mock(return_value=session)
    session.__exit__ = Mock(return_value=None)
    session.scalars().all = Mock(return_value=[question_a, question_c])

    get_engine.return_value = engine
    session_cls.return_value = session

    actual = get_questions(question_set="Places", db_path=Path("/my/database.sqlite"))

    assert actual == [question_a, question_c]

    get_engine.assert_called_once_with(Path("/my/database.sqlite"))
    select.assert_has_calls([call(Question), call().where(ANY)])
    session_cls.assert_called_once_with(engine)
    session.assert_has_calls(
        [
            call.scalars(select().where()),
            call.scalars().all(),
        ]
    )


@patch("flash_cards.orm.Session")
@patch("flash_cards.orm._get_engine")
def test_when_submit_game_then_correct_calls_made(get_engine, session_cls):
    game = Game()

    engine = Mock()
    session = Mock()
    session.__enter__ = Mock(return_value=session)
    session.__exit__ = Mock(return_value=None)

    get_engine.return_value = engine
    session_cls.return_value = session

    submit_game(game)

    get_engine.assert_called_once_with(None)
    session_cls.assert_called_once_with(engine)
    session.assert_has_calls([call.add(game), call.commit()])
