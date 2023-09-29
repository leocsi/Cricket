package minecraft.plugins;

import org.bukkit.event.Listener;
import org.bukkit.event.EventHandler;
import org.bukkit.event.entity.EntityDamageEvent;
import org.bukkit.event.player.PlayerLoginEvent;

import org.bukkit.entity.Player;

public class EventListener implements Listener {
    Plugin plugin;
    public EventListener(Plugin pluginClass){
        this.plugin = pluginClass;
        this.plugin.getServer().getPluginManager().registerEvents(this, plugin);
    }
    
    @EventHandler
    public void playerDamage(EntityDamageEvent e){
        if(e.getEntity() instanceof Player){
            Player player = (Player) e.getEntity();
            if (player.getDisplayName().equals("leocsi")){
                this.plugin.LOGGER.info("EventListener: Event happened!!!");
                String command = "room damage";
                this.plugin.getMessageSender().print(command);
                this.plugin.getMessageSender().flush();
            }
        }
    } 

    @EventHandler
    public void playerLoginEvent(PlayerLoginEvent e){
        this.plugin.LOGGER.info("EventListener: "+ e.getPlayer().getDisplayName() + " logged in!");
    }
}
