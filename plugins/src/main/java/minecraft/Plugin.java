package minecraft;

import java.util.logging.Logger;
import org.bukkit.plugin.java.JavaPlugin;

/*
 * plugins java plugin
 */
public class Plugin extends JavaPlugin
{
  private static final Logger LOGGER=Logger.getLogger("plugins");

  public void onEnable()
  {
    LOGGER.info("plugins enabled");
  }

  public void onDisable()
  {
    LOGGER.info("plugins disabled");
  }
}
