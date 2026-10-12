# Palette Structure Gate v0.13

## 目标
不只匹配“色相”，还必须匹配**明度体制、色数和面积角色**。

## 1. 必须记录
- background_value_regime: high / mid / low key
- chromatic_role_count
- background / dominant / secondary / accent
- 每个角色的面积、饱和度、明度

## 2. 来源优先级
1. Strong Lead
2. Style Pack
3. Concept
4. 活动语义（最低）

## 3. Hard RED
Strong Lead 下：
- high-key → low-key 或反向
- duotone/low-color → 4+ weighted chromatic roles
- Lead 无渐变却把多色渐变变成主要表达
- Support 引入新的全局主色体系

## 4. 主题色处理
主题色优先进入 Hero 内容，不默认进入 H0。
例如“敦煌色彩”可以出现在主视觉材料/流线，而不必让标题每字渐变。

## 5. 禁止 Semantic Color Shortcut
草坪=绿、户外=橙太阳+蓝云、儿童=彩虹、科技=蓝紫、传统=红金、沉浸=黑底发光，均无效。
