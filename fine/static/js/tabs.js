const tabsContainer = document.querySelectorAll(".tabs");
if (tabsContainer.length) {
  tabsContainer.forEach((container) => {
    const buttons = container.querySelectorAll("[name=tab-btn]");
    const contents = container.querySelectorAll("[id~=content-]");
    console.log(contents);
    if (buttons) {
      buttons.forEach((btn) => {
        btn.addEventListener("click", () => {
          contents.forEach((content) => content.classList.remove("active"));
          const containerNumber = Number(
            btn.getAttribute("id").replace("tab-btn-", "")
          );
          contents[containerNumber - 1].classList.add("active");
        });
      });
    }
  });
}
