from cli import cli
import cache
print(cache.cache.get("foo"))

cliTab = cli(20, 20)

cliTab.display()
