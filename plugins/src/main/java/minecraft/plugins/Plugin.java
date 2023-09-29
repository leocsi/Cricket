package minecraft.plugins;

import java.util.logging.Logger;
import org.bukkit.plugin.java.JavaPlugin;

import java.net.*;
import java.io.*;

/*
 * plugins java plugin
 */
public class Plugin extends JavaPlugin{
  Socket connection;
  PrintWriter messageSender;

  private static final Logger LOGGER=Logger.getLogger("plugins");

  public Plugin(){
    try{
      connection = new Socket("127.0.0.1", 65432); 
      messageSender = new PrintWriter(connection.getOutputStream(), true);
      LOGGER.info("HERE");
    } catch(Exception e){
      e.printStackTrace();
    }
  }

  public void onEnable()
  {
    messageSender.print("damage");
    LOGGER.info("plugin enabled");
  }

  public void onDisable()
  {
    LOGGER.info("plugin disabled");
    try{
      messageSender.close();
      connection.close();
    } catch(Exception e){
      e.printStackTrace();
    }
  }
}