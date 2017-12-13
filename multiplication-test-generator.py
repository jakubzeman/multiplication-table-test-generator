# -*- coding: utf-8 -*-
import itertools
import random
from flask import Flask, render_template, Markup, request, jsonify, send_from_directory


def generic_error_handler(error_object, status_code):
    """
    :param error_object: Exception object
    :type error_object: Exception
    :param status_code: HTTP error code
    :type status_code: int
    :rtype: object
    """
    resp_dict = {
        "success": False,
        "message": error_object.__class__.__name__ + ": " + str(error_object),
        "status_code": status_code
    }
    response = jsonify(resp_dict)
    response.status_code = status_code
    return response


class AppBaseException(Exception):
    status_code = 500

    def __init__(self, message, status_code=None, payload=None):
        """
        :param message: Exception message
        :type message: str
        :param status_code: HTTP status code
        :type status_code: int
        :param payload: JSON detailed info
        :type payload: dict
        """
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        """
        :rtype: dict
        """
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv

    def __str__(self):
        return self.message


class BadRequest(AppBaseException):
    def __init__(self, message, status_code=400, payload=None):
        AppBaseException.__init__(self, message, status_code, payload)


class InternalServerError(AppBaseException):
    def __init__(self, message, status_code=500, payload=None):
        AppBaseException.__init__(self, message, status_code, payload)


app = Flask(__name__)


@app.errorhandler(AppBaseException)
def handle_invalid_usage(error):
    return generic_error_handler(error, error.status_code)


def get_all_combinations_for_divisor(par_divisor):
    max_dividend = par_divisor * 10
    return [(par_divisor, num) for num in range(max_dividend + 1)]


def generate(small_number_set, exercise_count, remainder_word):
    all_combinations = [p + (p[0] * p[1],) for p in itertools.product(small_number_set, repeat=2)]
    ret = "<table cellpadding=\"10\" style=\"border-collapse: collapse;\">"
    for _ in range(exercise_count):
        exercise = random.choice(all_combinations)
        ret += "<tr><td>%2d</td> <td>x</td> <td>%2d</td> <td>=</td> <td></td> <td></td> </tr>" % (
            exercise[0],
            exercise[1]
        )

    ret += "<tr style=\"border-bottom: 1px solid black;\"><td></td> <td></td><td></td><td></td><td></td><td></td></tr>"

    for _ in range(exercise_count):
        exercise = random.choice(all_combinations)
        ret += "<tr><td>%2d</td> <td>:</td> <td>%2d</td> <td>=</td> <td></td> <td></td></tr>" % (
            exercise[2],
            exercise[1]
        )

    ret += "<tr style=\"border-bottom: 1px solid black;\"><td></td><td></td><td></td><td></td><td></td> <td></td></tr>"

    for _ in range(exercise_count):
        divisor = random.choice(small_number_set)
        exercise = random.choice(get_all_combinations_for_divisor(divisor))
        ret += "<tr><td>%2d</td><td>:</td><td>%2d</td><td>=</td><td style=\"%s\">%s</td><td>=</td></tr>" % (
            exercise[1],
            exercise[0],
            "padding: 10px 10px 10px 100px;",
            remainder_word
        )
    ret += "</table>"
    return Markup(ret)


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', test_source=generate(
        (2, 3, 4, 5, 6, 7, 8, 9),
        12,
        "Zbytek"
    ))


def splatky(pocet=84, castka=245000, sazba=3.99):
    zbytek = castka
    jistina = int(zbytek / pocet)
    sum_jistina = 0
    sum_urok = 0.0
    uroky = []
    for _ in range(pocet):
        urok = round((float(zbytek) * (sazba / 100.00)) / 12.00, 2)
        uroky.append(urok)
        zbytek -= jistina
        sum_urok += urok
        if castka - sum_jistina < jistina:
            jistina = castka - sum_jistina
            sum_jistina += jistina
            zbytek = 0
            # print("Splatka %.2f, jistina %d, urok %.2f" % (jistina + urok, jistina, urok))
            break
        else:
            sum_jistina += jistina
            # print("Splatka %.2f, jistina %d, urok %.2f" % (jistina + urok, jistina, urok))

    if zbytek > 0:
        urok = round((float(zbytek) * (sazba / 100.00)) / 12.00, 2)
        uroky[-1] += urok
        sum_urok += urok
        sum_jistina += zbytek
        # print("Splatka %.2f, jistina %d, urok %.2f" % (zbytek + urok, zbytek, urok))

    # print("Jistina celkem: %d, urok celkem %.2f (%.2f)" % (sum_jistina, sum_urok, sum(uroky)))
    sum_jistina_urok = int(sum_jistina + sum_urok)
    fixni_splatka = int(sum_jistina_urok / pocet)
    i = 0
    s_urok = 0.00
    s_jistina = 0
    ret = []
    # print(";splatka;jistina;urok")
    for urok in uroky:
        if i + 1 == pocet:
            row = {
                "poradi": i + 1,
                "splatka": (sum_jistina - s_jistina) + (sum_urok - s_urok),
                "jistina": sum_jistina - s_jistina,
                "urok": sum_urok - s_urok
            }
            """
            row = "%.2f;%.2f;%.2f" % (
                (sum_jistina - s_jistina) + (sum_urok - s_urok),
                sum_jistina - s_jistina,
                sum_urok - s_urok
            )
            """
        else:
            s_urok += urok
            s_jistina += fixni_splatka - urok
            row = {
                "poradi": i + 1,
                "splatka": fixni_splatka,
                "jistina": fixni_splatka - urok,
                "urok": urok
            }
            # row = "%d;%.2f;%.2f" % (fixni_splatka, fixni_splatka - urok, urok)
        i += 1
        # print("%d;%s" % (i, row.replace('.', ',')))
        ret.append(row)
    ret.append({
        "poradi": "Celkem",
        "splatka": sum_jistina + sum_urok,
        "jistina": sum_jistina,
        "urok": sum_urok
    })
    return ret


def check_json_content_type(http_request):
    """
    :param http_request: HTTP request
    :type http_request: flask.request
    :return: request's JSON body
    :rtype: dict
    """
    if not http_request.is_json:
        raise BadRequest("Unsupported Media Type", 415)
    json_body = http_request.get_json(silent=True)
    if json_body is None:
        raise BadRequest("Malformed JSON")
    return json_body


@app.route('/splatky/compute', methods=['POST'])
def splatky_compute():
    splatky_cfg = check_json_content_type(request)
    if 'pocet' not in splatky_cfg or 'castka' not in splatky_cfg or 'sazba' not in splatky_cfg:
        raise BadRequest("Jeden z konfiguracnich parametru splatky chybi.")

    return jsonify(splatky(
        splatky_cfg['pocet'],
        splatky_cfg['castka'],
        splatky_cfg['sazba']
    ))


@app.route('/splatky', methods=['GET'])
@app.route('/splatky/', methods=['GET'])
def splatky_get():
    return send_from_directory('templates', 'splatky.html')


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=22222, threaded=True)
    # app.run(debug=True)