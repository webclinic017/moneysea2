# coding=utf-8
import sys
import getopt
from moneysea.actions.baseaction import BaseAction
from moneysea.actions.typeaction import TypeAction
from moneysea.actions.priceaction import PriceAction

class HelpAction(BaseAction):
    def cmd(self):
        return "help"

    def summary(self):
        return "help information"

    def description(self):
        return '''
SYNOPSIS:
    python moneysea help [cmd]

DESCRIPTIONS:
    show help information for the specific command

OPTIONS:
    cmd
        specific command
'''

    def run(self, args, opts):
        if len(args) == 0:
            ms = MoneySea()
            ms.usage()

            print ""
            return
        ms = MoneySea()
        obj = ms.getaction(args[0])
        if obj == None:
            print "Unknown command:", args[0]
            return 
        print obj.description()


class MoneySea:
    def __init__(self):
        ########################################### add new actions here ########################################################
        self._version = "moneysea 0.4"
        self._actions = [TypeAction, PriceAction, HelpAction]
        self._options = ["verbose", "version"]
        pass

    def getaction(self, cmd):
        for action in self._actions:
            obj = action()
            if cmd == obj.cmd():
                return obj
        return None

    def getoptions(self):
        msg = ""
        for opt in self._options:
            msg += "[--" + opt + "]"
        return msg

    def usage(self):
        msg = "Usage: python moneysea " + self.getoptions()
        print ""
        print msg
        print "\t\t\tcommand [<args>]"

        print ""
        print "The most commonly used moneysea commands are:"
        for action in self._actions:
            obj = action()
            print "\t" + obj.cmd() + "\t\t" + obj.summary()

        print ""
        print "'python moneysea help cmd' show command details"
        print ""

    def optionversion(self, opts):
        for opt, a in opts:
            if "--version" == opt:
                return True
        return False


    def run(self):
        try:
            opts, args = getopt.getopt(sys.argv[1:], "", self._options)
            if self.optionversion(opts):
                print self._version
                sys.exit(0)

            if len(args) == 0:
                print "No command is specified"
                raise Exception("no command")

            obj = self.getaction(args[0])
            if obj == None:
                print "Unknown command:", args[0]
                raise Exception("unknown command")
        except Exception as e:
#            print e
            self.usage()
            sys.exit(2)

        obj.run(args[1:], opts)

if __name__ == "__main__":
    if sys.getdefaultencoding() != 'utf-8':
        reload(sys)
        sys.setdefaultencoding('utf-8')
    ms = MoneySea()
    ms.run()
