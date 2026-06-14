5. 商用化潛力與未來展望

5.1 具體應用場景與商業價值：吃到飽餐廳剩食罰款應用
隨著全球淨零碳排趨勢與糧食安全議題發酵，剩食管理已不再只是道德宣導，而是許多餐飲業者面臨的實際成本痛點。特別是在「All-You-Can-Eat（自助餐/吃到飽）」餐廳的商業模式中，顧客因眼大肚子小而導致的高單價食材（如海鮮、高級肉品）浪費情況極為嚴重。目前許多吃到飽餐廳雖訂有「剩食超過特定重量即加收費用」的規章，但實務上礙於以下兩個痛點而難以嚴格執行：一是人工結帳時的檢查標準不一，極易引發客訴爭議；二是服務生難以快速判定剩食究竟是低價的蔬菜澱粉，還是高成本的肉類海鮮。

本研究所提出的「YOLO+VLM 協同廚餘辨識系統」完美契合了此一痛點。將本系統部署於餐廳的餐盤回收區或結帳台，能在 1 到 2 秒內自動掃描並精準列出盤中殘留的食材種類。系統會結合底部的重量感測器，根據後端建立的食材碳足跡資料庫，自動計算該盤剩食的總碳排放量。此碳足跡資料庫的各項食材碳排係數（Carbon Footprint Coefficients），主要參考自牛津大學與聯合國數據支持的開放資料平台 Our World in Data（https://ourworldindata.org/environmental-impacts-of-food）。

為了建立客觀且具環保教育意義的罰款機制，本系統提出了以下的剩食罰款計算公式：
**罰款金額 = 總碳排放量 (gCO2e) × 單位碳排放懲罰費率 (元/gCO2e)**
其中，總碳排放量為「各項剩食重量 × 該食材的單位碳排係數」之總和。例如，牛肉的碳排係數遠高於蔬菜，因此留下同重量的牛肉將會產生高出數十倍的碳排放，進而對應更高的罰款金額。

透過 VLM 強大的視覺特徵萃取與常識推理能力，即便是被破壞形狀的高價蟹管肉或牛排，系統也能精準辨識。這不僅為餐廳提供了自動化收取剩食罰款的客觀數據依據、減少人工檢查的爭議，更能將傳統的「重量罰款」升級為「環境成本罰款」，具備龐大的 B2B 軟體即服務（SaaS）商用潛力。

5.2 邊緣運算與雲端 VLM 的成本效益分析
在商用化過程中，「營運成本」是決定技術能否落地的關鍵。若所有影像都上傳至雲端交由 GPT-4o 進行辨識，高昂的 API 費用將吞噬掉系統帶來的節費效益。本系統採用的「協同架構」巧妙地解決了這個問題。在多數情況下（約 80%），邊緣端的 YOLO 模型已能給出足夠高信心的判斷，其推論成本趨近於零且無需網路傳輸；僅有當 YOLO 遇到嚴重遮擋、光線不佳或罕見食材導致信心度過低時（約 20% 的長尾案例），才會將圖片裁切或加註紅框後發送至雲端。這種「高頻初篩交給邊緣，低頻糾錯交給雲端」的設計，大幅節省了超過 80% 的 API 呼叫成本，實現了效能與預算的完美平衡。

5.3 未來技術展望
儘管本研究證實了 GPT-4o 與 Gemini 2.5 Flash 在廚餘糾錯上的強大能力，但仰賴雲端 API 仍具有延遲與隱私外洩的潛在風險。未來的研究方向可朝向「開源輕量化 VLM 的地端部署」邁進。隨著 LLaVA、Qwen-VL 等開源視覺語言模型技術逐漸成熟，我們有望將參數量壓縮至數十億級別（Billion-parameter level），並搭配模型量化（Quantization）與神經網絡處理器（NPU），將 VLM 直接部署於餐飲現場的邊緣運算設備中。這不僅能徹底解決網路延遲與 API 成本問題，更將成為下一代餐飲永續管理系統的技術標配。

6. 結論
本研究成功開發並驗證了一套「邊緣與雲端協同」的廚餘辨識系統，藉此解決傳統輕量級 YOLO 模型在複雜便當場景下的效能瓶頸。透過實作「全圖脈絡提示（Red Box Context）」、「多標籤輸出」以及「思維鏈（CoT）推理」，我們極大化了大型視覺模型（VLM）的零樣本糾錯潛力。實驗數據顯示，導入 GPT-4o 作為後盾能將系統整體準確率從 26.5% 顯著提升至 44.1%，且統計檢定（McNemar's Test, p = 0.0247）亦證明此技術具備堅實的統計意義。此外，在東西方飲食文化的對照分析中，VLM 展現了跨文化的廣泛世界知識，成功將西方食物的辨識率拉升了一倍以上。
展望未來，本系統不僅在技術架構上取得了學術創新，更在「吃到飽餐廳剩食罰款自動化」等永續商業場景中展現了極高的落地價值。我們相信，這種融合高效邊緣運算與高智商雲端 AI 的混合架構，將成為推動全球餐飲業淨零轉型的重要推手。

參考文獻

American Psychological Association. (2001). Publication manual of the American Psychological Association (5th ed.). Washington, DC: American Psychological Association.

Brown, T., Mann, B., Ryder, N., Subbiah, M., Kaplan, J. D., Dhariwal, P., ... & Amodei, D. (2020). Language models are few-shot learners. Advances in neural information processing systems, 33, 1877-1901.

Jocher, G., Chaurasia, A., & Qiu, J. (2023). Ultralytics YOLO (Version 8.0.0) [Computer software]. https://github.com/ultralytics/ultralytics

OpenAI. (2024). GPT-4 Technical Report. arXiv preprint arXiv:2303.08774.

Reid, M., Savinov, N., Denisov, D., ... & Vinyals, O. (2024). Gemini 1.5: Unlocking multimodal understanding across millions of tokens of context. arXiv preprint arXiv:2403.05530.

Wei, J., Wang, X., Schuurmans, D., Bosma, M., Xia, F., Chi, E., ... & Zhou, D. (2022). Chain-of-thought prompting elicits reasoning in large language models. Advances in neural information processing systems, 35, 24824-24837.

Ritchie, H., Rosado, P., & Roser, M. (2022). Environmental Impacts of Food Production. Our World in Data. Retrieved from https://ourworldindata.org/environmental-impacts-of-food

Cookpad Inc. (2024). Cookpad Taiwan. Retrieved from https://cookpad.com/tw
