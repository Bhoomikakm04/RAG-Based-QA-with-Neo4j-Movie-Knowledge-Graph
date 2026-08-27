(function () {
  // Small client-side enhancement. PyVis supplies the full graph JavaScript;
  // this adds a smooth reveal class to the embedded application document.
  try {
    document.documentElement.classList.add('graphrag-ready');
  } catch (e) {}
})();
