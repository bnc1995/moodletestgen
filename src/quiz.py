import xml.etree.ElementTree as ET
from name import Name
from unitgradingtype import Unitgradingtype
from unitpenalty import Unitpenalty
from showunits import Showunits
from unitsleft import Unitsleft
from question import Question
from subquestion import Subquestion
from answer import Answer
import gen_rand_input
import json


class Quiz(ET.Element):
    '''Quiz class for moodle quiz
        :param config: json config file

    '''
    def __init__(self, config = None):
        super(Quiz, self).__init__('quiz')

        #config json file
        self.config = json.load(config)

    def gen_questions(self):
        '''generate quiz based on config file

        '''
        for i in range(0, self.config['number_of_questions']):

            #generate new question
            question = Question(self.config['type'])
            #set question name
            question.set_name(self.config['name'])

            #generate input parameters of question. The values will be between the minimum and maximum values and rounded to that decimal places what is in the config file.
            input = gen_rand_input.gen_rand_input(self.config['input_parameters'])

            #Format qustion text. Replace the markers with the input parameters
            question.set_questiontext(self.config['questiontext'].format(*input))

            #generate subquestions and their answers
            for q in self.config['questions']:
                #import answers module
                #the answer generator function have to be in a module. The modules and funcions name must be same and it is in the config file
                module = __import__(q['answer'])

                #call the answer generator function with the generated input parameters
                answer = Answer(eval('module.' + q['answer'] + '(input)'), q['fraction'])

                #new subguestion
                subquestion = Subquestion(q['question'], answer)

                #add subquestion to question
                question.add_subquestion(subquestion)

            #add question to quiz
            self.add_question(question)

    def add_question(self, question):
        '''add question to quiz
            :param question: moodle question (Question)

        '''
        self.append(question)

    def write(self):
        '''write quiz to file (moodle XML format)

        '''
        tree = ET.ElementTree(self)

        tree.write(self.config['output_file'], 'utf-8')
