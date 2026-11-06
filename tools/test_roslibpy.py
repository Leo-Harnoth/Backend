import roslibpy

c = roslibpy.Ros(host='localhost', port=9090)
c.run()
T = 'assistant_interfaces/srv/'
get = roslibpy.Service(c, '/assistant/get_preferences', T + 'GetPreferences')
set_ = roslibpy.Service(c, '/assistant/set_preferences', T + 'SetPreferences')
print('vorher :', get.call(roslibpy.ServiceRequest({'user_id': 1}))['language'])
print('setzen :', set_.call(roslibpy.ServiceRequest({'user_id': 1, 'language': 'en'})))
print('nachher:', get.call(roslibpy.ServiceRequest({'user_id': 1}))['language'])
c.terminate()
