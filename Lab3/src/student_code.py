import read, copy
from util import *
from logical_classes import *

verbose = 0

class KnowledgeBase(object):
    def __init__(self, facts=[], rules=[]):
        self.facts = facts
        self.rules = rules
        self.ie = InferenceEngine()

    def __repr__(self):
        return 'KnowledgeBase({!r}, {!r})'.format(self.facts, self.rules)

    def __str__(self):
        string = "Knowledge Base: \n"
        string += "\n".join((str(fact) for fact in self.facts)) + "\n"
        string += "\n".join((str(rule) for rule in self.rules))
        return string

    def _get_fact(self, fact):
        """INTERNAL USE ONLY
        Get the fact in the KB that is the same as the fact argument

        Args:
            fact (Fact): Fact we're searching for

        Returns:
            Fact: matching fact
        """
        for kbfact in self.facts:
            if fact == kbfact:
                return kbfact

    def _get_rule(self, rule):
        """INTERNAL USE ONLY
        Get the rule in the KB that is the same as the rule argument

        Args:
            rule (Rule): Rule we're searching for

        Returns:
            Rule: matching rule
        """
        for kbrule in self.rules:
            if rule == kbrule:
                return kbrule

    def kb_add(self, fact_rule):
        """Add a fact or rule to the KB

        Args:
            fact_rule (Fact|Rule) - the fact or rule to be added

        Returns:
            None
        """
        result_ = fact_rule
        printv("Adding {!r}", 1, verbose, [fact_rule])
        if isinstance(fact_rule, Fact):
            if fact_rule not in self.facts:
                self.facts.append(fact_rule)
                for rule in self.rules:
                    self.ie.fc_infer(fact_rule, rule, self)
            else:
                if fact_rule.supported_by:
                    ind = self.facts.index(fact_rule)
                    result_ = self.facts[ind]
                    for f in fact_rule.supported_by:
                        self.facts[ind].supported_by.append(f)

        elif isinstance(fact_rule, Rule):
            if fact_rule not in self.rules:
                self.rules.append(fact_rule)
                for fact in self.facts:
                    self.ie.fc_infer(fact, fact_rule, self)
            else:
                if fact_rule.supported_by:
                    ind = self.rules.index(fact_rule)
                    result_ = self.rules[ind]
                    for f in fact_rule.supported_by:
                        self.rules[ind].supported_by.append(f)
        return result_

    def kb_assert(self, statement):
        """Assert a fact or rule into the KB

        Args:
            statement (Statement): Statement we're asserting in the format produced by read.py
        """
        printv("Asserting {!r}", 0, verbose, [statement])
        self.kb_add(Fact(statement) if factq(statement) else Rule(statement))

    def kb_ask(self, statement):
        """Ask if a fact is in the KB

        Args:
            statement (Statement) - Statement to be asked (will be converted into a Fact)

        Returns:
            listof Bindings|False - list of Bindings if result found, False otherwise
        """
        printv("Asking {!r}", 0, verbose, [statement])
        if factq(statement):
            f = Fact(statement)
            bindings_lst = ListOfBindings()
            # ask matched facts
            for fact in self.facts:
                binding = match(f.statement, fact.statement)
                if binding:
                    bindings_lst.add_bindings(binding, [fact])

            return bindings_lst if bindings_lst.list_of_bindings else False

        else:
            print "Invalid ask:", statement
            return False

    def kb_retract(self, statement):
        """Retract a fact from the KB

        Args:
            statement (Statement) - Statement to be asked (will be converted into a Fact)

        Returns:
            None
        """

        printv("Retracting {!r}", 0, verbose, [statement])
        ####################################################
        # Student code goes here

        f0 = Fact(statement)
        f= self._get_fact(f0)
        #print f
        if f.asserted and f.supported_by == []:
            f.asserted = False
            self.kb_retract1(f)
        elif f.asserted and f.supported_by != []:
            f.asserted = False
            for r1, f1 in f.supported_by:
                # print 'bbbbbb'
                if isinstance(f, Rule):
                    r1.supports_rules.remove(f)
                    f1.supports_rules.remove(f)
                if isinstance(f, Fact):
                    r1.supports_facts.remove(f)
                    f1.supports_facts.remove(f)
        else:
            self.kb_retract1(f)

    def kb_del(self, fr):
        if isinstance(fr, Fact):
            self.facts.remove(fr)
        else:
            self.rules.remove(fr)

    def kb_retract1(self, f):
        if f.supported_by != []:

            for r1, f1 in f.supported_by:
                # print 'bbbbbb'
                if isinstance(f, Rule):
                    r1.supports_rules.remove(f)
                    f1.supports_rules.remove(f)

                if isinstance(f, Fact):
                    r1.supports_facts.remove(f)
                    f1.supports_facts.remove(f)

        # print f.supports_facts

        if f.supports_facts != []:
            for f2 in f.supports_facts:
                if not f2.asserted :


                    if len(f2.supported_by) == 1:


                        self.kb_retract1(f2)

                    else:
                        for r11, f11 in f2.supported_by:
                            if isinstance(f, Rule):
                                if r11 == f:
                                    f2.supported_by.remove([r11, f11])
                            if isinstance(f, Fact):
                                if f11 == f:
                                    f2.supported_by.remove([r11, f11])
            # print f.supports_rules
        if f.supports_rules != []:
            for f2 in f.supports_rules:

                if not f2.asserted :


                    if len(f2.supported_by) == 1:

                        self.kb_retract1(f2)

                    else:
                        for r11, f11 in f2.supported_by:
                            if isinstance(f, Rule):
                                if r11 == f:
                                    f2.supported_by.remove([r11, f11])
                            if isinstance(f, Fact):
                                if f11 == f:
                                    f2.supported_by.remove([r11, f11])

        self.kb_del(f)










class InferenceEngine(object):
    def fc_infer(self, fact, rule, kb):
        """Forward-chaining to infer new facts and rules

        Args:
            fact (Fact) - A fact from the KnowledgeBase
            rule (Rule) - A rule from the KnowledgeBase
            kb (KnowledgeBase) - A KnowledgeBase

        Returns:
            Nothing
        """
        printv('Attempting to infer from {!r} and {!r} => {!r}', 1, verbose,
            [fact.statement, rule.lhs, rule.rhs])
        ####################################################
        # Student code goes here
        fs=rule.lhs[0]

        #print fs

        binding = match(fs,fact.statement)

        #print binding

        supported_by0 = [[rule, fact]]
        if binding:
            if len(rule.lhs) == 1:
                a = 0
                new_fact = Fact(instantiate(rule.rhs, binding),supported_by0)
                #
                # for f in kb.facts:
                #     if f.statement == instantiate(rule.rhs, binding):
                #
                #         rule.supports_facts.append(new_fact)
                #         fact.supports_facts.append(new_fact)
                #         f.supported_by=supported_by0
                #         #print f
                #         a = a+1
                # if a == 0:
                new_fact=kb.kb_add(new_fact)
                rule.supports_facts.append(new_fact)
                fact.supports_facts.append(new_fact)


            else:
                lhs_list = []
                for s in rule.lhs[1:]:
                    lhs_list.append(instantiate(s,binding))

                    #binding1 = match(s, fact.statement)
                new_rule = Rule([lhs_list,instantiate(rule.rhs,binding)], supported_by0)

                # for r in self.rules:
                #     if r.statement == instantiate(rule.rhs, binding):

                #         rule.supports_rules.append(new_rule)
                #         fact.supports_rules.append(new_rule)
                # #print lhs_list
                # #print instantiate(rule.rhs,binding)
                # else:
                new_rule=kb.kb_add(new_rule)
                rule.supports_rules.append(new_rule)
                fact.supports_rules.append(new_rule)















