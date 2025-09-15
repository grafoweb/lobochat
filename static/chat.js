(function(){
  const BRAND = "Lobo and Company";
  const ORIGIN = window.location.origin;
  const API_CHAT = ORIGIN + "/chat";
  const AVATAR = ORIGIN + "/static/avatar.jpg";

  const css = `.lobo-chat-launcher{position:fixed;bottom:20px;right:20px;width:64px;height:64px;border-radius:50%;overflow:hidden;}`;
  const style = document.createElement('style');
  style.innerHTML = css; document.head.appendChild(style);

  const launcher = document.createElement('button');
  launcher.className = 'lobo-chat-launcher';
  launcher.innerHTML = `<img src="${AVATAR}" alt="${BRAND}">`;
  document.body.appendChild(launcher);
})();