from flask.json import JSONEncoder


class Local(object):
    new_id = 1

    def __init__(self, nome, endereco, capacidade_maxima):
        self.id = Local.new_id
        self.nome = nome
        self.endereco = endereco
        self.capacidade_maxima = capacidade_maxima

        Local.new_id += 1


class Agendamento(object):
    new_id = 1

    def __init__(self, nome, data_inicio, data_final, local_id):
        self.id = Agendamento.new_id
        self.nome = nome
        self.data_inicio = data_inicio
        self.data_final = data_final
        self.local_id = local_id


class UsersEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Local):
            return obj.__dict__
        return super(UsersEncoder, self).default(obj)
