# Open WebUI 主题和透明度调节功能开发计划

**任务：** 添加若干主题（粉色系、绿色系、蓝色系、宝石系），并允许用户通过设置菜单调节侧边栏、消息气泡和聊天背景的透明度。

**目标：**

1.  添加粉色系、绿色系、蓝色系、宝石系主题。
2.  在设置菜单中添加透明度调节选项，控制侧边栏、消息气泡和聊天背景的透明度。

**计划步骤：**

1.  **创建新的主题 CSS 文件：**
    *   在 `static/themes/` 目录下创建新的 CSS 文件，例如 `pink.css`, `green.css`, `blue.css`, `gem.css` , 'gemini.css' , 'golden.css' 。
    *   在这些文件中定义新主题的颜色变量和样式，参考 `rosepine.css` 的结构。

2.  **更新主题列表：**
    *   修改 `src/lib/components/chat/Settings/General.svelte` 中的 `themes` 数组，添加新主题的名称。

3.  **修改 `applyTheme` 函数：**
    *   更新 `src/lib/components/chat/Settings/General.svelte` 中的 `applyTheme` 函数，使其能够正确应用新主题的 CSS 类。

4.  **修改 `Settings` 类型定义：**
    *   在 `src/lib/stores/index.ts` 的 `Settings` 类型定义中添加新的可选属性，例如 `sidebarOpacity`, `bubbleOpacity`, `backgroundOpacity`，类型为 `number`。

5.  **在 General 设置组件中添加透明度调节 UI：**
    *   修改 `src/lib/components/chat/Settings/General.svelte`，在界面中添加滑块或输入框，用于调节侧边栏、消息气泡和聊天背景的透明度。
    *   将这些调节的值绑定到 `settings` store 中新添加的透明度属性。

6.  **应用透明度样式：**
    *   找到负责渲染侧边栏、消息气泡和聊天背景的 Svelte 组件（根据之前的搜索结果，可能在 `src/lib/components/layout/Sidebar.svelte`, `src/lib/components/chat/Messages/Message.svelte`, `src/lib/components/chat/Chat.svelte` 等文件中）。
    *   修改这些组件的样式，使其根据 `settings` store 中的透明度值应用 `opacity` 样式。这可能需要在元素的 style 属性中动态绑定透明度值，或者根据透明度值添加/移除特定的 CSS 类。

7.  **保存透明度设置：**
    *   确保在 `src/lib/components/chat/Settings/General.svelte` 的 `saveHandler` 函数中，将透明度设置的值正确地保存到 `settings` store 和用户设置中。

**Mermaid 图示：**

```mermaid
graph TD
    A[用户任务: 添加主题和透明度调节] --> B(分析现有代码结构)
    B --> C{找到主题和设置相关文件?}
    C -- 是 --> D(读取相关文件内容)
    D --> E{找到主题列表和应用逻辑?}
    E -- 是 --> F{找到设置UI和Settings类型?}
    F -- 是 --> G(制定详细计划)
    G --> H(创建新主题CSS文件)
    H --> I(更新主题列表)
    I --> J(修改applyTheme函数)
    J --> K(修改Settings类型定义)
    K --> L(添加透明度调节UI)
    L --> M(应用透明度样式)
    M --> N(保存透明度设置)
    N --> O(完成)
    C -- 否 --> P(使用搜索工具查找)
    E -- 否 --> P
    F -- 否 --> P
    P --> D