from .models import Profile

V = Profile.STYLE_VISUAL
A = Profile.STYLE_AURAL
R = Profile.STYLE_READ_WRITE
K = Profile.STYLE_KINESTHETIC
M = Profile.STYLE_MULTIMODAL


class QuizQuestion:

    def __init__(self, text, options):
        self.text = text
        self.options = options


class LearningStyleQuiz:

    def __init__(self, quiz_questions):
        self.questions = quiz_questions


class QuizOption:

    def __init__(self, text, style):
        self.text = text
        self.style = style

    def __str__(self):
        return 'Option: ' + self.text + '__ style:' + self.style


class LearningStyle:

    def __init__(self, visual, aural, read_write, kinesthetic):
        self.v = visual
        self.a = aural
        self.r = read_write
        self.k = kinesthetic

    def get_main_style_code(self):
        values = [(self.v, V),
                  (self.a, A),
                  (self.r, R),
                  (self.k, K)]

        # sorting the results
        results = sorted(values, reverse=True)  # the first element is the most important

        # checks if it is a multimodal style
        if results[0][0] == results[1][0]:
            return Profile.STYLE_MULTIMODAL

        return results[0][1]  # kod czytanie / pisanie / inne..

    def __str__(self):
        return (
                'v=' + str(self.v) +
                ', a=' + str(self.a) +
                ', r=' + str(self.r) +
                ', k=' + str(self.k) +
                ' main_style=' + self.get_main_style_code()
        )


# based on classes - building the right objects with specific values
learning_style_quiz = LearningStyleQuiz(
    [
        QuizQuestion('1. I need to find the way to a shop that a friend has recommended. I would:', [
            QuizOption('find out where the shop is in relation to somewhere I know.', K),
            QuizOption('ask my friend to tell me the directions.', A),
            QuizOption('write down the street directions I need to remember.', R),
            QuizOption('use a map.', V),
        ]),
        QuizQuestion('2. A website has a video showing how to make a special graph or chart. '
                     'There is a person speaking, some lists and words describing what to do and some diagrams. I would learn most from:',
                     [
                         QuizOption('seeing the diagrams.', V),
                         QuizOption('listening.', A),
                         QuizOption('reading the words.', R),
                         QuizOption('watching the actions.', K),
                     ]),
        QuizQuestion('3. I want to find out more about a tour that I am going on. I would:', [
            QuizOption('look at details about the highlights and activities on the tour', K),
            QuizOption('use a map and see where the places are.', V),
            QuizOption('read about the tour on the itinerary.', R),
            QuizOption('talk with the person who planned the tour or others who are going on the tour.', A),
        ]),
        QuizQuestion('4. When choosing a career or area of study, these are important for me:', [
            QuizOption('Applying my knowledge in real situations. ', K),
            QuizOption('Communicating with others through discussion. ', A),
            QuizOption('Working with designs, maps or charts. ', V),
            QuizOption('Using words well in written communications. ', R),
        ]),
        QuizQuestion('5. When I am learning I:', [
            QuizOption('like to talk things through.', A),
            QuizOption('see patterns in things. ', V),
            QuizOption('use examples and applications. ', K),
            QuizOption('read books, articles and handouts. ', R),
        ]),
        QuizQuestion('6. I want to save more money and to decide between a range of options. I would:', [
            QuizOption('consider examples of each option using my financial information. ', K),
            QuizOption('read a print brochure that describes the options in detail. ', R),
            QuizOption('use graphs showing different options for different time periods. ', V),
            QuizOption('talk with an expert about the options. ', A),
        ]),
        QuizQuestion('7. I want to learn how to play a new board game or card game. I would:', [
            QuizOption('watch others play the game before joining in. ', K),
            QuizOption('listen to somebody explaining it and ask questions.', A),
            QuizOption('use the diagrams that explain the various stages, moves and strategies in the game. ', V),
            QuizOption('read the instructions.', R),
        ]),
        QuizQuestion('8. I have a problem with my heart. I would prefer that the doctor:', [
            QuizOption('gave me something to read to explain what was wrong', R),
            QuizOption('used a plastic model to show me what was wrong. ', K),
            QuizOption('described what was wrong. ', A),
            QuizOption('showed me a diagram of what was wrong. ', V),
        ]),
        QuizQuestion('9. I want to learn to do something new on a computer. I would:', [
            QuizOption('read the written instructions that came with the program. ', R),
            QuizOption('talk with people who know about the program.', A),
            QuizOption('start using it and learn by trial and error. ', K),
            QuizOption('follow the diagrams in a book.', V),
        ]),
        QuizQuestion('10. When learning from the Internet I like:', [
            QuizOption('videos showing how to do or make things. ', K),
            QuizOption('interesting design and visual features. ', V),
            QuizOption('interesting written descriptions, lists and explanations. ', R),
            QuizOption('audio channels where I can listen to podcasts or interviews. ', A),
        ]),
        QuizQuestion('11. I want to learn about a new project. I would ask for:', [
            QuizOption('diagrams to show the project stages with charts of benefits and costs. ', V),
            QuizOption('a written report describing the main features of the project. ', R),
            QuizOption('an opportunity to discuss the project.', A),
            QuizOption('examples where the project has been used successfully.', K),
        ]),
        QuizQuestion('12. I want to learn how to take better photos. I would:', [
            QuizOption('ask questions and talk about the camera and its features. ', A),
            QuizOption('use the written instructions about what to do.', R),
            QuizOption('use diagrams showing the camera and what each part does. ', V),
            QuizOption('use examples of good and poor photos showing how to improve them. ', K),
        ]),
        QuizQuestion('13. I prefer a presenter or a teacher who uses:', [
            QuizOption('demonstrations, models or practical sessions. ', K),
            QuizOption('question and answer, talk, group discussion, or guest speakers. ', A),
            QuizOption('handouts, books, or readings. ', R),
            QuizOption('diagrams, charts, maps or graphs. ', V),
        ]),
        QuizQuestion('14. I have finished a competition or test and I would like some feedback.'
                     ' I would like to have feedback:', [
                         QuizOption('using examples from what I have done.', K),
                         QuizOption('using a written description of my results. ', R),
                         QuizOption('from somebody who talks it through with me.', A),
                         QuizOption('using graphs showing what I achieved. ', V),
                     ]),
        QuizQuestion('15. I want to find out about a house or an apartment. Before visiting it I would want:', [
            QuizOption('to view a video of the property.', K),
            QuizOption('a discussion with the owner. ', A),
            QuizOption('a printed description of the rooms and features. ', R),
            QuizOption('a plan showing the rooms and a map of the area. ', V),
        ]),
        QuizQuestion('16. I want to assemble a wooden table that came in parts (kitset). I would learn best from:', [
            QuizOption('diagrams showing each stage of the assembly. ', V),
            QuizOption('advice from someone who has done it before. ', A),
            QuizOption('written instructions that came with the parts for the table. ', R),
            QuizOption('watching a video of a person assembling a similar table. ', K),
        ]),
    ]
)


def is_valid(quiz, data):
    for question_nr in range(len(quiz.questions)):
        counter = 0

        for option_nr in range(4):
            checkbox_name = "question_" + str(question_nr) + "_" + str(option_nr)
            value = data.get(checkbox_name)
            if value == "on":
                counter += 1

        if counter == 0:
            return False
    return True


def process_quiz(quiz, data):
    visual = 0
    aural = 0
    read_write = 0
    kinesthetic = 0

    question_nr = 0
    for question in quiz.questions:

        for option_nr in range(4):
            checkbox_name = "question_" + str(question_nr) + "_" + str(option_nr)
            if data.get(checkbox_name) == "on":
                option = question.options[option_nr]

                if option.style == V:
                    visual += 1
                elif option.style == A:
                    aural += 1
                elif option.style == R:
                    read_write += 1
                elif option.style == K:
                    kinesthetic += 1
        question_nr += 1

    return LearningStyle(visual, aural, read_write, kinesthetic)


def render_quiz(quiz, data=None):
    if data is None:
        data = {}

    html = ''

    i = 0
    for question in quiz.questions:
        html += '<p>' + question.text + '</p>'
        html += '\n'

        # display all options for each question
        nr = 0
        for option in question.options:
            # get value for each checkbox
            checkbox_name = "question_" + str(i) + "_" + str(nr)
            value = data.get(checkbox_name)

            html += "<div>"

            # display checkbox based on value
            if value == "on":
                html += '<input type="checkbox" name="' + checkbox_name + '" checked>'
            else:
                html += '<input type="checkbox" name="' + checkbox_name + '">'

            html += ' <label for="' + checkbox_name + '">' + option.text + '</label>'
            html += '</div>'

            html += '\n'
            nr += 1

        html += '</select>'
        html += '\n'
        i += 1
    return html
