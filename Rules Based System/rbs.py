def trap_mf(a, b, c, d, x):
    return max(0, min((x - a) / (b - a), 1, (d - x) / (d - c)))


class FuzzySet:

    def __init__(self, variable, name, mf, a, b, c, d):
        self.variable = variable
        self.name = name
        self.mf = mf
        self.a = a
        self.b = b
        self.c = c
        self.d = d

    def fuzzify(self, x):
        return self.mf(self.a, self.b, self.c, self.d, x)


class FuzzyVariable:

    def __init__(self, name):
        self.name = name
        self.sets = {}

    def add_set(self, set):
        self.sets[set.name] = set

    def fuzzify(self, x):
        dict = {}
        for i in self.sets.keys():
            dict[i] = self.sets[i].fuzzify(x)
        return dict


class FuzzyRule:

    def __init__(self, variable, name):
        self.sets = {}
        self.name = name
        self.variable = variable

    def add_set(self, set):
        self.sets[set.name] = set

    def evaluate(self, inputs):
        value = 1
        for i in inputs.keys():
            for j in self.sets.values():
                if j.variable == i:
                    value = min(value, j.fuzzify(inputs[i]))
                    break
        return value


class FuzzySystem:

    def __init__(self, output_variable):
        self.variables = {}
        self.output_variable = output_variable
        self.rules = []

    def add_rule(self, rule):
        self.rules.append(rule)

    def add_variable(self, variable):
        self.variables[variable.name] = variable

    def compute(self, inputs):
        output_dict = {}
        for i in self.output_variable.sets.keys():
            output_dict[i] = 0

        for i in self.rules:
            output_dict[i.name] = max(output_dict[i.name], i.evaluate(inputs))

        print(output_dict)

        gradient = {}
        for i in self.output_variable.sets.values():
            if i.b not in gradient:
                gradient[i.b] = []
                gradient[i.b].append(i.name)
            else:
                if i.name not in gradient[i.b]:
                    gradient[i.b].append(i.name)

            if i.c not in gradient:
                gradient[i.c] = []
                gradient[i.c].append(i.name)
            else:
                if i.name not in gradient[i.c]:
                    gradient[i.c].append(i.name)

        print(gradient)

        weighted_total = 0
        weights = 0
        for i in gradient.keys():
            value = 0
            for j in gradient[i]:
                value = max(value, output_dict[j])
            print(value)
            weighted_total += value*i
            weights += value

        return weighted_total/weights


if __name__ == '__main__':

    temperature = FuzzyVariable("temperature")

    s1 = FuzzySet("temperature", "very cold", trap_mf, -1000, -30, -20, 5)
    s2 = FuzzySet("temperature", "cold", trap_mf, -5, 0, 0, 10)
    s3 = FuzzySet("temperature", "normal", trap_mf, 5, 10, 15, 20)
    s4 = FuzzySet("temperature", "warm", trap_mf, 15, 20, 20, 25)
    s5 = FuzzySet("temperature", "hot", trap_mf, 25, 30, 35, 1000)

    temperature.add_set(s1)
    temperature.add_set(s2)
    temperature.add_set(s3)
    temperature.add_set(s4)
    temperature.add_set(s5)

    humidity = FuzzyVariable("humidity")

    s6 = FuzzySet("humidity", "dry", trap_mf, -1000, 0, 0, 50)
    s7 = FuzzySet("humidity", "normal", trap_mf, 0, 50, 50, 100)
    s8 = FuzzySet("humidity", "wet", trap_mf, 50, 100, 100, 1000)

    humidity.add_set(s6)
    humidity.add_set(s7)
    humidity.add_set(s8)

    time = FuzzyVariable("time")

    s9 = FuzzySet("time", "short", trap_mf, -1000, 0, 0, 50)
    s10 = FuzzySet("time", "medium", trap_mf, 0, 50, 50, 100)
    s11 = FuzzySet("time", "long", trap_mf, 50, 100, 100, 1000)

    time.add_set(s9)
    time.add_set(s10)
    time.add_set(s11)

    r1 = FuzzyRule("time", "short")
    r1.add_set(s1)
    r1.add_set(s8)

    r2 = FuzzyRule("time", "short")
    r2.add_set(s2)
    r2.add_set(s8)

    r3 = FuzzyRule("time", "short")
    r3.add_set(s3)
    r3.add_set(s8)

    r4 = FuzzyRule("time", "short")
    r4.add_set(s4)
    r4.add_set(s8)

    r5 = FuzzyRule("time", "medium")
    r5.add_set(s5)
    r5.add_set(s8)

    r6 = FuzzyRule("time", "short")
    r6.add_set(s1)
    r6.add_set(s7)

    r7 = FuzzyRule("time", "medium")
    r7.add_set(s2)
    r7.add_set(s7)

    r8 = FuzzyRule("time", "medium")
    r8.add_set(s3)
    r8.add_set(s7)

    r9 = FuzzyRule("time", "medium")
    r9.add_set(s4)
    r9.add_set(s7)

    r10 = FuzzyRule("time", "long")
    r10.add_set(s5)
    r10.add_set(s7)

    r11 = FuzzyRule("time", "medium")
    r11.add_set(s1)
    r11.add_set(s6)

    r12 = FuzzyRule("time", "long")
    r12.add_set(s2)
    r12.add_set(s6)

    r13 = FuzzyRule("time", "long")
    r13.add_set(s3)
    r13.add_set(s6)

    r14 = FuzzyRule("time", "long")
    r14.add_set(s4)
    r14.add_set(s6)

    r15 = FuzzyRule("time", "long")
    r15.add_set(s5)
    r15.add_set(s6)

    sys = FuzzySystem(time)
    sys.add_variable(temperature)
    sys.add_variable(humidity)
    sys.add_rule(r1)
    sys.add_rule(r2)
    sys.add_rule(r3)
    sys.add_rule(r4)
    sys.add_rule(r5)
    sys.add_rule(r6)
    sys.add_rule(r7)
    sys.add_rule(r8)
    sys.add_rule(r9)
    sys.add_rule(r10)
    sys.add_rule(r11)
    sys.add_rule(r12)
    sys.add_rule(r13)
    sys.add_rule(r14)
    sys.add_rule(r15)

    print(sys.compute({"humidity": 75, "temperature": 10  }))

















