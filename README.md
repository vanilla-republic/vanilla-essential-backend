# vanilla-essential-backend
Common backend utils developed and used by Vanilla Republic 🍀

# docker-compose.yml explanation
* support Cloudflare tunnel for exposing your local (home lab) service to the internet
    * if you don't need this feature, comment them out
* `vanilla_essential_backend_storage` : the volume (also any other volume) can be mounted onto external SSD
    * if you don't need this feature, comment them out
* Vanilla Republic don't usually expose port onto host machine due to Cloudflare service presence
    * if you need such exposure, please consider add them in your running docker