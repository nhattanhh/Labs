function render(content, data) {
  return content.replace(/{{(.*?)}}/g, function(match, expression) {
      return eval(expression); 
  });
}
