from endstone.plugin import Plugin
from endstone.command import Command, CommandSender
from endstone import ColorFormat
from endstone.event import event_handler, PlayerJoinEvent


"""
Working plugin template
"""
class TestPlugin(Plugin):
    api_version = "0.5"

    def on_load(self) -> None:
        self.logger.info("on_load is called!")

    def on_enable(self) -> None:
        self.logger.info("on_enable is called!")
        self.register_events(self) # register the event handler - by calling self.register_events, Endstone will look into the object that is passed in as the argument and register all handlers with a @event_handler decorator to the event system.
        self.server.scheduler.run_task(self, self.say_hi, delay= 0, period= 100) # every 100 ticks self.say_hi executes
    def on_disable(self) -> None:
        self.logger.info("on_disable is called!")

    commands = {
        "hello" : {
            "description" : "Greet the command sender",
            "usages" : ["/hello (formal|friend|family)<action: GreetAction>"],
            "permissions" : ["test_plugin.command.hello"]
        }
    }

    permissions = {
        "test_plugin.command.hello" : {
            "description" : "Allow users to use the /hello command",
            "default" : "op",
        }
    }

    def on_command(self, sender: CommandSender, command: Command, args: list[str]) -> bool:
        self.logger.info(str(args)) # for debugging
        if command.name == "hello":
            if len(args) == 0 or (len(args) == 1 and args[0] == ""):
                sender.send_message(f"{ColorFormat.DARK_AQUA}Hello {ColorFormat.GOLD}world!")
            else:
                sender.send_message(f"{ColorFormat.BOLD}{ColorFormat.DARK_GREEN}{args[0]}")

        return True
    
    @event_handler  # decorator - basically says when on_player_join happens use this function to handle the event
    def on_player_join(self, event: PlayerJoinEvent):       # event : PlayerJoinEvent is a type hint - basically it says that parameter event should be of type PlayerJoinEvent
        self.server.broadcast_message(f"{ColorFormat.YELLOW}{event.player.name} has joined the server")

    def say_hi(self) -> None:
        for player in self.server.online_players:
            player.send_popup("Hi")
            player.send_title("COOL STUFF", "is this cool?", fade_in= 20, fade_out= 20)
            player.send_toast("Notification", "Get your life toghether!")
       