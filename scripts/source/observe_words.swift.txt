// OCR an explicitly supplied public image. No app/window inspection or inputs.
import Foundation
import Vision
guard CommandLine.arguments.count == 2 else {
    fputs("Usage: observe_words IMAGE\n", stderr)
    exit(2)
}
let url = URL(fileURLWithPath: CommandLine.arguments[1])
let request = VNRecognizeTextRequest()
request.recognitionLevel = .accurate
request.usesLanguageCorrection = false
try VNImageRequestHandler(url: url).perform([request])
let pattern = try NSRegularExpression(pattern: "\\S+")
func box(_ rect: CGRect, _ text: String) -> [String: Any] {
    return ["text": text, "x": rect.minX, "y": 1 - rect.maxY,
            "w": rect.width, "h": rect.height]
}
let rows = (request.results ?? []).compactMap { result -> [String: Any]? in
    guard let best = result.topCandidates(1).first else { return nil }
    var row = box(result.boundingBox, best.string)
    row["words"] = pattern.matches(in: best.string,
        range: NSRange(best.string.startIndex..., in: best.string)).compactMap { match -> [String: Any]? in
        guard let range = Range(match.range, in: best.string),
              let bounds = try? best.boundingBox(for: range) else { return nil }
        return box(bounds.boundingBox, String(best.string[range]))
    }
    return row
}
let data = try JSONSerialization.data(withJSONObject: rows, options: [.sortedKeys])
print(String(data: data, encoding: .utf8)!)
