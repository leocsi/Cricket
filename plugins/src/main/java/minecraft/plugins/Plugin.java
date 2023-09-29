package minecraft.plugins;

import java.util.logging.Logger;
import org.bukkit.plugin.java.JavaPlugin;

import java.net.*;
import java.io.*;

/*
 * plugins java plugin
 */
public class Plugin extends JavaPlugin{
  private Socket connection;
  public PrintWriter messageSender;

  public final Logger LOGGER=Logger.getLogger("plugins");

  public Plugin(){
    try{
      this.connection = new Socket("127.0.0.1", 65432); 
      this.messageSender = new PrintWriter(connection.getOutputStream(), true);
      LOGGER.info("Connected!");
    } catch(Exception e){
      e.printStackTrace();
    }
  }

  public void onEnable()
  {
    new EventListener(this);
  }

  public void onDisable()
  {
    LOGGER.info("plugin disabled");
    try{
      this.messageSender.close();
      this.connection.close();
    } catch(Exception e){
      e.printStackTrace();
    }
  }

  public PrintWriter getMessageSender(){
    return this.messageSender;
  }
}