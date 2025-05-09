import pytest
from model import Question, Choice


def test_create_question():
    question = Question(title='q1')
    assert question.id != None

def test_create_multiple_questions():
    question1 = Question(title='q1')
    question2 = Question(title='q2')
    assert question1.id != question2.id

def test_create_question_with_invalid_title():
    with pytest.raises(Exception):
        Question(title='')
    with pytest.raises(Exception):
        Question(title='a'*201)
    with pytest.raises(Exception):
        Question(title='a'*500)

def test_create_question_with_valid_points():
    question = Question(title='q1', points=1)
    assert question.points == 1
    question = Question(title='q1', points=100)
    assert question.points == 100

def test_create_choice():
    question = Question(title='q1')
    
    question.add_choice('a', False)

    choice = question.choices[0]
    assert len(question.choices) == 1
    assert choice.text == 'a'
    assert not choice.is_correct

def test_question_with_invalid_points():
    with pytest.raises(Exception):
        Question(title='q1', points=0)
    with pytest.raises(Exception):
        Question(title='q1', points=101)

def test_add_multiple_choices():
    question = Question(title='q1')
    question.add_choice('a', False)
    question.add_choice('b', True)
    question.add_choice('c', False)
    
    assert len(question.choices) == 3
    assert question.choices[1].text == 'b'
    assert question.choices[1].is_correct == True

def test_remove_choice_by_id():
    question = Question(title='q1')
    choice1 = question.add_choice('a', False)
    choice2 = question.add_choice('b', True)
    
    question.remove_choice_by_id(choice1.id)
    assert len(question.choices) == 1
    assert question.choices[0].id == choice2.id

def test_remove_all_choices():
    question = Question(title='q1')
    question.add_choice('a', False)
    question.add_choice('b', True)
    question.add_choice('c', False)
    
    question.remove_all_choices()
    assert len(question.choices) == 0

def test_choice_ids_are_incremental():
    question = Question(title='q1')
    choice1 = question.add_choice('a')
    choice2 = question.add_choice('b')
    choice3 = question.add_choice('c')
    
    assert choice1.id == 1
    assert choice2.id == 2
    assert choice3.id == 3

def test_select_choices_within_max_selections():
    question = Question(title='q1', max_selections=2)
    choice1 = question.add_choice('a', True)
    choice2 = question.add_choice('b', False)
    choice3 = question.add_choice('c', True)
    
    selected = question.select_choices([choice1.id, choice3.id])
    assert len(selected) == 2
    assert choice1.id in selected
    assert choice3.id in selected

def test_select_choices_exceeding_max_selections():
    question = Question(title='q1', max_selections=1)
    choice1 = question.add_choice('a', True)
    choice2 = question.add_choice('b', False)
    
    with pytest.raises(Exception):
        question.select_choices([choice1.id, choice2.id])

def test_set_correct_choices():
    question = Question(title='q1')
    choice1 = question.add_choice('a', False)
    choice2 = question.add_choice('b', False)
    choice3 = question.add_choice('c', False)
    
    question.set_correct_choices([choice1.id, choice3.id])
    assert question.choices[0].is_correct == True
    assert question.choices[1].is_correct == False
    assert question.choices[2].is_correct == True

def test_select_choices_returns_only_correct_selections():
    question = Question(title='q1', max_selections=3)
    choice1 = question.add_choice('a', True)
    choice2 = question.add_choice('b', False)
    choice3 = question.add_choice('c', True)
    
    selected = question.select_choices([choice1.id, choice2.id, choice3.id])
    assert len(selected) == 2
    assert choice1.id in selected
    assert choice2.id not in selected
    assert choice3.id in selected

def test_create_choice_with_invalid_text():
    with pytest.raises(Exception):
        Choice(id=1, text='')
    with pytest.raises(Exception):
        Choice(id=1, text='a'*101)

@pytest.fixture
def multiple_choice_question():
    question = Question(title="Multiple choice question", points=10, max_selections=3)
    choice1 = question.add_choice("First option", True)
    choice2 = question.add_choice("Second option", False)
    choice3 = question.add_choice("Third option", True)
    choice4 = question.add_choice("Fourth option", False)
    return {
        "question": question,
        "choices": [choice1, choice2, choice3, choice4],
        "correct_choices": [choice1, choice3]
    }

@pytest.fixture
def single_choice_question():
    question = Question(title="Single choice question", points=5, max_selections=1)
    choice1 = question.add_choice("Option A", False)
    choice2 = question.add_choice("Option B", True)
    choice3 = question.add_choice("Option C", False)
    return {
        "question": question,
        "choices": [choice1, choice2, choice3],
        "correct_choice": choice2
    }

def test_correct_choice_selection_with_fixture(multiple_choice_question):
    question = multiple_choice_question["question"]
    choices = multiple_choice_question["choices"]
    correct_choices = multiple_choice_question["correct_choices"]
    
    correct_choice_ids = [choice.id for choice in correct_choices]
    
    selected = question.select_choices(correct_choice_ids)
    
    assert len(selected) == len(correct_choice_ids)
    for id in correct_choice_ids:
        assert id in selected

def test_max_selections_with_fixture(single_choice_question):
    question = single_choice_question["question"]
    choices = single_choice_question["choices"]
    
    with pytest.raises(Exception, match=f"Cannot select more than {question.max_selections} choices"):
        question.select_choices([choice.id for choice in choices])
    
    correct_choice = single_choice_question["correct_choice"]
    selected = question.select_choices([correct_choice.id])
    assert len(selected) == 1
    assert selected[0] == correct_choice.id

def test_points_configuration_with_fixtures(multiple_choice_question, single_choice_question):
    multi_question = multiple_choice_question["question"]
    single_question = single_choice_question["question"]
    
    assert multi_question.points == 10
    assert single_question.points == 5
    
    assert 1 <= multi_question.points <= 100
    assert 1 <= single_question.points <= 100